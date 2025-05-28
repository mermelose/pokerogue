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
    ("Volcano", "Beach"),
    ("Volcano", "Badlands"),
    ("Badlands", "Wasteland"),
    ("Badlands", "Abyss"),
    ("Beach", "Sea"),
    ("Sea", "Island"),
    ("Island", "Seabed"),
    ("Seabed", "Fairy Cave"),
    ("Fairy Cave", "Ice Cave"),
    ("Ice Cave", "Snowy Forest"),
    ("Snowy Forest", "Meadow"),
    ("Meadow", "Forest"),
    ("Forest", "Graveyard"),
    ("Swamp", "Graveyard"),
    ("Graveyard", "Abyss"),
    ("Abyss", "Town"),
    ("Cave", "Lake"),
    ("Lake", "Meadow"),
    ("Wasteland", "Badlands"),
    ("Space", "Mountain")
    ]

# Añadir aristas al grafo
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
def encontrar_ciclo_mas_corto(grafo, nodo):
    """Encuentra el ciclo más corto que comienza y termina en el nodo dado."""
    try:
        vecinos = list(grafo.successors(nodo))
        ciclo_minimo = None
        longitud_minima = float('inf')
        
        for vecino in vecinos:
            try:
                camino = nx.shortest_path(grafo, source=vecino, target=nodo)
                longitud_actual = len(camino) + 1
                
                if longitud_actual < longitud_minima:
                    longitud_minima = longitud_actual
                    ciclo_minimo = [nodo] + camino
            except nx.NetworkXNoPath:
                continue
        
        if ciclo_minimo:
            return ciclo_minimo
        else:
            raise nx.NetworkXNoCycle
    except nx.NetworkXError:
        raise nx.NetworkXNoCycle
# Función para calcular rutas (adaptada para múltiples destinos)
def calcular_rutas(inicio, destinos, stage_actual, stage_primer_lider):
    resultados = []
    for destino in destinos:
        try:
            if inicio == destino:
                ciclo = encontrar_ciclo_mas_corto(grafo, inicio)
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
                        pos = nx.spring_layout(G, seed=42)
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
