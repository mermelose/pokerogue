import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(layout="wide", page_title="Pokerogue - Multi-Ruta")

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
    st.header("Configuración de Ruta")
    
    # Modo de selección
    modo_seleccion = st.radio(
        "Tipo de destino:",
        ["Único bioma", "Múltiples biomas"],
        index=0
    )
    
    # Bioma de inicio (siempre único)
    inicio = st.selectbox("Bioma de inicio:", biomas, index=biomas.index("Town"))
    
    # Selector de destino según modo
    if modo_seleccion == "Único bioma":
        destino = st.selectbox("Bioma de destino:", biomas, index=biomas.index("Town"))
        destinos = [destino]
    else:
        st.markdown("**Selecciona varios biomas:**")
        destinos = []
        cols = st.columns(3)
        for i, bioma in enumerate(biomas):
            with cols[i % 3]:
                if st.checkbox(bioma, key=f"bioma_{bioma}"):
                    destinos.append(bioma)
    
    # Configuración de stages
    st.subheader("Configuración de Stages")
    stage_actual = st.number_input("Stage actual:", min_value=1, value=1)
    stage_primer_lider = st.radio(
        "Stage del primer líder:",
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
                "destino": destino,
                "saltos": saltos,
                "camino": " → ".join(camino),
                "lider": lider
            })
        except (nx.NetworkXNoPath, nx.NetworkXNoCycle):
            resultados.append({
                "destino": destino,
                "error": f"No hay ruta a {destino}"
            })
    return resultados

# Botón de cálculo
if st.button("Calcular Rutas", type="primary"):
    if not destinos:
        st.warning("¡Selecciona al menos un bioma de destino!")
    else:
        resultados = calcular_rutas(inicio, destinos, stage_actual, stage_primer_lider)
        
        # Mostrar resultados en pestañas
        tabs = st.tabs([f"Ruta a {res['destino']}" for res in resultados])
        
        for tab, res in zip(tabs, resultados):
            with tab:
                if "error" in res:
                    st.error(res["error"])
                else:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Bioma destino", res["destino"])
                        st.metric("Saltos necesarios", res["saltos"])
                    with col2:
                        st.metric("Líder al llegar", "✅ Sí" if res["lider"] else "❌ No")
                    
                    st.subheader("Camino:")
                    st.code(res["camino"])
                    
                    # Visualización gráfica (opcional)
                    with st.expander("Ver mapa de ruta"):
                        fig, ax = plt.subplots(figsize=(10, 8))
                        pos = {
                            "Town": (0, 0),
                            "Grassy Field": (1, 0),
                            "Tall Grass": (2, 0),
                            "Forest": (3, 0),
                            "Meadow": (4, 0),
                            "Plains": (1, -1),
                            "Metropolis": (0, -1),
                            "Slum": (0, -2),
                            "Swamp": (1, -2),
                            "Construction Site": (2, -2),
                            "Power Plant": (3, -2),
                            "Factory": (4, -2),
                            "Laboratory": (5, -2),
                            "Dojo": (2, -1),
                            "Jungle": (3, 1),
                            "Temple": (4, 1),
                            "Desert": (5, 1),
                            "Ancient Ruins": (6, 1),
                            "Mountain": (7, 1),
                            "Volcano": (8, 1),
                            "Wasteland": (8, 0),
                            "Space": (7, 2),
                            "Fairy Cave": (5, 0),
                            "Ice Cave": (6, 0),
                            "Snowy Forest": (6, -1),
                            "Lake": (3, -1),
                            "Beach": (4, -1),
                            "Sea": (5, -1),
                            "Island": (6, -2),
                            "Seabed": (7, -2),
                            "Badlands": (8, -1),
                            "Cave": (4, -3),
                            "Graveyard": (2, -3.5),
                            "Abyss": (3, -4),
                        }

                        nx.draw(G, pos, with_labels=True, ax=ax, node_size=300, font_size=6)
                        
                        if "camino" in res:
                            camino_nodos = res["camino"].split(" → ")
                            edge_list = [(camino_nodos[i], camino_nodos[i+1]) for i in range(len(camino_nodos)-1)]
                            nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='r', width=2)
                            nx.draw_networkx_nodes(G, pos, nodelist=camino_nodos, node_color='r', node_size=500)
                        
                        st.pyplot(fig)

# Instrucciones
with st.expander("ℹ️ Instrucciones"):
    st.markdown("""
    **Cómo usar:**
    1. Selecciona el bioma de inicio
    2. Elige entre ruta única o múltiples destinos
    3. Configura los stages
    4. Haz clic en "Calcular Rutas"
    
    **Modo múltiples biomas:**
    - Selecciona varios biomas con los checkboxes
    - Los resultados se mostrarán en pestañas separadas
    """)
