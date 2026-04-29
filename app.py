import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(layout="wide", page_title="Pokerogue Shortest Route Calculator")

# Función para cargar el grafo (la misma que tenías)
def cargar_grafo():
    G = nx.DiGraph()
    biomas = [
        "Dojo", "Jungle", "Temple", "Desert", "Ancient Ruins", "Space",
        "Fairy Cave", "Ice Cave", "Mountain", "Volcano", "Beach", "Sea",
        "Island", "Seabed", "Wasteland", "Badlands", "Cave", "Lake",
        "Snowy Forest", "Meadow", "Forest", "Construction Site", "Laboratory",
        "Factory", "Power Plant", "Slum", "Metropolis", "Plains", "Grassy Field",
        "Tall Grass", "Swamp", "Graveyard", "Abyss", "Town"
    ]
    G.add_nodes_from(biomas)
   
    edges = [
    ("Town", "Plains"),
    ("Plains", "Grassy Field"), ("Plains", "Lake"), ("Plains", "Metropolis"),
    ("Grassy Field", "Tall Grass"),
    ("Tall Grass", "Forest"),
    ("Tall Grass", "Cave"),
    ("Metropolis","Slum"),
    ("Slum","Swamp"),
    ("Slum","Construction Site"),
    ("Construction Site","Power Plant"),
    ("Construction Site","Dojo"),
    ("Power Plant","Factory"),
    ("Factory","Laboratory"),
    ("Factory","Plains"),
    ("Laboratory","Construction Site"),
    ("Dojo","Jungle"),
    ("Dojo","Temple"),
    ("Dojo","Plains"),
    ("Jungle","Temple"),
    ("Temple","Swamp"),
    ("Temple","Desert"),
    ("Temple","Ancient Ruins"),
    ("Desert","Ancient Ruins"),
    ("Ancient Ruins","Mountain"),
    ("Ancient Ruins","Forest"),
    ("Mountain", "Volcano"),
    ("Mountain", "Wasteland"),
    ("Mountain", "Space"),
    ("Forest","Jungle"),
    ("Forest","Meadow"),
    ("Meadow","Plains"),
    ("Meadow","Fairy Cave"),
    ("Fairy Cave","Ice Cave"),
    ("Fairy Cave","Space"),
    ("Ice Cave","Snowy Forest"),
    ("Snowy Forest","Forest"),
    ("Snowy Forest","Mountain"),
    ("Snowy Forest","Lake"),
    ("Lake","Beach"),
    ("Lake","Swamp"),
    ("Lake","Construction Site"),
    ("Beach","Sea"),
    ("Beach","Island"),
    ("Swamp","Graveyard"),
    ("Swamp","Tall Grass"),
    ("Graveyard","Abyss"),
    ("Abyss","Cave"),
    ("Abyss","Space"),
    ("Abyss","Wasteland"),
    ("Wasteland","Badlands"),
    ("Cave","Laboratory"),
    ("Cave","Lake"),
    ("Cave","Badlands"),
    ("Sea","Seabed"),
    ("Sea","Ice Cave"),
    ("Island","Sea"),
    ("Seabed","Cave"),
    ("Seabed","Volcano"),
    ("Badlands","Desert"),
    ("Badlands","Mountain"),
    ("Volcano","Beach"),
    ("Volcano","Ice Cave"),
    ("Space","Ancient Ruins")
    ]
    G.add_edges_from(edges)
    return G, biomas

# Cargar el grafo y lista de biomas
G, biomas = cargar_grafo()

# Sidebar con controles
with st.sidebar:
    st.header("Route Configuration")
   
    # Modo de selección
    modo_seleccion = st.radio(
        "Target Search Mode:",
        ["Single biome", "Multiple biomes"],
        index=0
    )
   
    # Bioma de inicio (siempre único)
    inicio = st.selectbox("Start Biome:", biomas, index=biomas.index("Town"))
   
    # Selector de destino según modo
    if modo_seleccion == "Single biome":
        destino = st.selectbox("Target Biome:", biomas, index=biomas.index("Town"))
        destinos = [destino]
    else:
        st.markdown("**Select one or more target biomes:**")
        destinos = []
        cols = st.columns(3)
        for i, bioma in enumerate(biomas):
            with cols[i % 3]:
                if st.checkbox(bioma, key=f"bioma_{bioma}"):
                    destinos.append(bioma)
   
    # Configuración de stages
    st.subheader("Stage Config")
    stage_actual = st.number_input("Current Stage(Stage/10):", min_value=1, value=1)
    stage_primer_lider = st.radio(
        "Stage with first Gym Leader:",
        [2, 3],
        index=0,
        horizontal=True
    )

# Función para calcular rutas (adaptada para múltiples destinos)
def calcular_rutas(inicio, destinos, stage_actual, stage_primer_lider):
    resultados = []
    for destino in destinos:
        try:
            if inicio == destino:
                ciclo = nx.shortest_cycle(G, source=inicio)
                saltos = len(ciclo) - 1
                camino = ciclo
            else:
                camino = nx.shortest_path(G, source=inicio, target=destino)
                saltos = len(camino) - 1
           
            stage_al_llegar = stage_actual + saltos
            lider = (stage_al_llegar >= stage_primer_lider) and ((stage_al_llegar - stage_primer_lider) % 3 == 0)
           
            resultados.append({
                "target": destino,
                "steps": saltos,
                "path": " → ".join(camino),
                "leader": lider
            })
        except (nx.NetworkXNoPath, nx.NetworkXNoCycle):
            resultados.append({
                "target": destino,
                "error": f"No route found to {destino}"
            })
    return resultados

# Botón de cálculo
if st.button("Calculate Routes", type="primary"):
    if not destinos:
        st.warning("¡Select at least one target biome!")
    else:
        resultados = calcular_rutas(inicio, destinos, stage_actual, stage_primer_lider)
       
        # Mostrar resultados en pestañas
        tabs = st.tabs([f"Route to {res['target']}" for res in resultados])
       
        for tab, res in zip(tabs, resultados):
            with tab:
                if "error" in res:
                    st.error(res["error"])
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Target Biome", res["target"])
                        st.metric("Steps needed", res["saltos"])
                    with col2:
                        st.metric("Is the boss stage a Gym Leader?", "✅ Sí" if res["lider"] else "❌ No")
                   
                    st.subheader("Route:")
                    st.code(res["camino"])
                   
                    # Visualización gráfica (opcional)
                    with st.expander("See route map"):
                        fig, ax = plt.subplots(figsize=(10, 8))
                        pos = nx.spring_layout(G, seed=42)
                        nx.draw(G, pos, with_labels=True, ax=ax, node_size=300, font_size=6)
                       
                        if "camino" in res:
                            camino_nodos = res["camino"].split(" → ")
                            edge_list = [(camino_nodos[i], camino_nodos[i+1]) for i in range(len(camino_nodos)-1)]
                            nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='r', width=2)
                            nx.draw_networkx_nodes(G, pos, nodelist=camino_nodos, node_color='r', node_size=500)
                       
                        st.pyplot(fig)

# Instructions
with st.expander("ℹ️ Instructions"):
    st.markdown("""
    **How to use:**
    1. Select the start biome
    2. Choose between single or multiple destinations
    3. Set the stages
    4. Click "Calculate Routes"
   
    **Multiple biomes mode:**
    - Select several biomes using the checkboxes
    - Results will appear in separate tabs
    """)
