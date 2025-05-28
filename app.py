

import matplotlib.pyplot as plt

import streamlit as st
import networkx as nx

# Función original (con la solución alternativa para shortest_cycle)
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

def saltos_y_lider_al_llegar(grafo, inicio, destino, stage_actual, stage_primer_lider):
    if inicio == destino:
        try:
            ciclo = encontrar_ciclo_mas_corto(grafo, inicio)
            saltos = len(ciclo) - 1
            camino = ciclo
            
            stage_al_llegar = stage_actual + saltos
            habra_lider_al_llegar = (stage_al_llegar >= stage_primer_lider) and ((stage_al_llegar - stage_primer_lider) % 3 == 0)
            
            return saltos, camino, habra_lider_al_llegar
        except nx.NetworkXNoCycle:
            return -1, [], False
    else:
        try:
            camino = nx.shortest_path(grafo, source=inicio, target=destino)
            saltos = len(camino) - 1
            stage_al_llegar = stage_actual + saltos
            habra_lider_al_llegar = (stage_al_llegar >= stage_primer_lider) and ((stage_al_llegar - stage_primer_lider) % 3 == 0)
            return saltos, camino, habra_lider_al_llegar
        except nx.NetworkXNoPath:
            return -1, [], False

# Configuración de la app Streamlit
st.title("Pokerogue - Consulta de Rutas entre Biomas")

# Crear el grafo (copiado de tu notebook)
G = nx.DiGraph()
biomas = [
    "Dojo", "Jungle", "Temple", "Desert", "Ancient Ruins", "Space", "Fairy Cave", "Ice Cave",
    "Mountain", "Volcano", "Beach", "Sea", "Island", "Seabed", "Wasteland", "Badlands",
    "Cave", "Lake", "Snowy Forest", "Meadow", "Forest", "Construction Site", "Laboratory",
    "Factory", "Power Plant", "Slum", "Metropolis", "Plains", "Grassy Field", "Tall Grass",
    "Swamp", "Graveyard", "Abyss", "Town"
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

# Sidebar para los inputs
with st.sidebar:
    st.header("Parámetros de Búsqueda")
    
    # Selección de biomas (manual o desplegable)
    input_method = st.radio("Selección de biomas:", ["Desplegable", "Manual"])
    
    if input_method == "Desplegable":
        inicio = st.selectbox("Bioma de inicio:", biomas, index=biomas.index("Town"))
        destino = st.selectbox("Bioma de destino:", biomas, index=biomas.index("Town"))
    else:
        inicio = st.text_input("Bioma de inicio:", "Town")
        destino = st.text_input("Bioma de destino:", "Town")
    
    # Stage actual con botones +/-
    st.subheader("Stage Actual")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("-1"):
            if 'stage_actual' not in st.session_state:
                st.session_state.stage_actual = 1
            st.session_state.stage_actual = max(1, st.session_state.stage_actual - 1)
    with col2:
        stage_actual = st.number_input(
            "Valor:", 
            min_value=1, 
            value=1 if 'stage_actual' not in st.session_state else st.session_state.stage_actual,
            key="stage_input"
        )
    with col3:
        if st.button("+1"):
            if 'stage_actual' not in st.session_state:
                st.session_state.stage_actual = 1
            st.session_state.stage_actual += 1
    
    # Stage primer líder (radio buttons)
    st.subheader("Stage del Primer Líder")
    stage_primer_lider = st.radio(
        "Seleccione:",
        [2, 3],
        index=0,
        horizontal=True
    )

# Botón para ejecutar la consulta
if st.button("Calcular Ruta"):
    # Validar que los biomas existen
    if inicio not in biomas or destino not in biomas:
        st.error("¡Alguno de los biomas no existe en el grafo!")
    else:
        saltos, camino, lider = saltos_y_lider_al_llegar(
            G, inicio, destino, stage_actual, stage_primer_lider
        )
        
        if saltos == -1:
            st.error(f"No hay camino desde {inicio} hasta {destino}")
        else:
            st.success(f"**Resultados para {inicio} → {destino}**")
            
            col_res1, col_res2 = st.columns(2)
            with col_res1:
                st.metric("Saltos necesarios", saltos)
            with col_res2:
                st.metric("Líder al llegar", "Sí" if lider else "No")
            
            st.subheader("Camino más corto:")
            st.write(" → ".join(camino))
            
            # Visualización del grafo (opcional)
            st.subheader("Visualización del Grafo")
            fig, ax = plt.subplots(figsize=(12, 8))
            pos = nx.spring_layout(G, seed=42)
            nx.draw(G, pos, with_labels=True, ax=ax, node_size=500, font_size=8)
            
            # Resaltar el camino
            if len(camino) > 1:
                edge_list = [(camino[i], camino[i+1]) for i in range(len(camino)-1)]
                nx.draw_networkx_edges(G, pos, edgelist=edge_list, edge_color='r', width=2)
                nx.draw_networkx_nodes(G, pos, nodelist=camino, node_color='r', node_size=700)
            
            st.pyplot(fig)

# Instrucciones
st.markdown("""
**Instrucciones:**
1. Selecciona o escribe los biomas de inicio y destino
2. Ajusta el stage actual con los botones +/-
3. Selecciona en qué stage apareció el primer líder (2 o 3)
4. Haz clic en "Calcular Ruta"
""")
