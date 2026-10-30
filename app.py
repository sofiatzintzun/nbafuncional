import streamlit as st
import pandas as pd

# Configuración general de la página
st.set_page_config(
    page_title="Panel de Análisis Deportivo",
    page_icon="🏀",
    layout="wide"
)

# Menú lateral de navegación
st.sidebar.title("Navegación")
menu = st.sidebar.radio("Selecciona una sección:", ["Equipos", "Jugadores", "Partidos"])

# URLs de cada pestaña de Google Sheets
URL_EQUIPOS = "https://docs.google.com/spreadsheets/d/1RiInl1AnLDp1haLz0uMP8jsa04AppRzt8xhGSJLw7gQ/export?format=csv&gid=0"
URL_JUGADORES = "https://docs.google.com/spreadsheets/d/1RiInl1AnLDp1haLz0uMP8jsa04AppRzt8xhGSJLw7gQ/export?format=csv&gid=417439193"
URL_PARTIDOS = "https://docs.google.com/spreadsheets/d/1RiInl1AnLDp1haLz0uMP8jsa04AppRzt8xhGSJLw7gQ/export?format=csv&gid=561826503"

# Función con caché para cargar los datos de forma rápida
@st.cache_data(ttl=300)
def cargar_datos(url):
    df = pd.read_csv(url)
    return df

# Buscador general en la barra lateral
st.sidebar.markdown("---")
busqueda = st.sidebar.text_input("🔍 Buscar en la vista actual:", "")

# ---------------------------------------------------------
# VISTA 1: EQUIPOS (Diseño en Tarjetas Visuales)
# ---------------------------------------------------------
if menu == "Equipos":
    st.title("🏆 Vista de Equipos")
    st.markdown("Panel visual de equipos activos.")
    
    try:
        df_equipos = cargar_datos(URL_EQUIPOS)
        
        # Filtrar la columna G (índice 6) para mostrar solo los diferentes a "No Juega Hoy"
        if len(df_equipos.columns) > 6:
            col_g = df_equipos.columns[6]
            df_equipos = df_equipos[df_equipos[col_g].astype(str).str.strip().str.lower() != "no juega hoy"]
        
        if busqueda:
            mascara = df_equipos.astype(str).apply(lambda row: row.str.contains(busqueda, case=False).any(), axis=1)
            df_equipos = df_equipos[mascara]

        st.metric("Equipos Mostrados", len(df_equipos))
        st.markdown("---")

        # Iterar sobre cada fila para crear una tarjeta visual personalizada
        for index, row in df_equipos.iterrows():
            with st.container(border=True):
                # Dividimos la tarjeta en columnas: Izquierda para Imagen, Derecha para la info
                col_img, col_info = st.columns([1, 4])
                
                # Asignación según las columnas de tu esquema (ajusta los nombres si es necesario)
                # J = Imagen, B = Nombre, C,D,E,F = Estadísticas, H = Descripción, I = Reporte de jugadores
                
                with col_img:
                    # Intenta mostrar la imagen de la columna J (o ajusta el nombre de tu columna de imagen)
                    try:
                        imagen_url = row.iloc[9] # Índice 9 corresponde a la columna J
                        if pd.notna(imagen_url) and str(imagen_url).startswith("http"):
                            st.image(imagen_url, width=100)
                        else:
                            st.write("🏀")
                    except:
                        st.write("🏀")

                with col_info:
                    # Nombre (Columna B / Índice 1)
                    nombre_equipo = row.iloc[1] if len(row) > 1 else "Equipo"
                    st.subheader(f"{nombre_equipo}")
                    
                    # Estadísticas (Columnas C, D, E, F / Índices 2, 3, 4, 5)
                    try:
                        c_stat2 = df_equipos.columns[2]
                        d_stat3 = df_equipos.columns[3]
                        e_stat4 = df_equipos.columns[4]
                        f_stat5 = df_equipos.columns[5]
                        
                        stat_cols = st.columns(4)
                        with stat_cols[0]:
                            st.metric(label=str(c_stat2), value=str(row.iloc[2]))
                        with stat_cols[1]:
                            st.metric(label=str(d_stat3), value=str(row.iloc[3]))
                        with stat_cols[2]:
                            st.metric(label=str(e_stat4), value=str(row.iloc[4]))
                        with stat_cols[3]:
                            st.metric(label=str(f_stat5), value=str(row.iloc[5]))
                    except Exception as err:
                        st.text("Estadísticas no disponibles")

                    st.markdown("---")
                    
                    # Descripción (Columna H / Índice 7) y Reporte de jugadores (Columna I / Índice 8)
                    desc_col, rep_col = st.columns(2)
                    with desc_col:
                        try:
                            desc_val = row.iloc[7] if len(row) > 7 else ""
                            st.markdown(f"**Descripción:** {desc_val}")
                        except:
                            pass
                            
                    with rep_col:
                        try:
                            rep_val = row.iloc[8] if len(row) > 8 else ""
                            st.markdown(f"**Reporte de Jugadores:** {rep_val}")
                        except:
                            pass

    except Exception as e:
        st.error(f"Error al cargar la pestaña Equipos: {e}")

# ---------------------------------------------------------
# VISTA 2: JUGADORES
# ---------------------------------------------------------
elif menu == "Jugadores":
    st.title("🏃 Vista de Jugadores")
    st.markdown("Rendimiento, uso y estadísticas individuales de los jugadores.")
    
    try:
        df_jugadores = cargar_datos(URL_JUGADORES)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Filas (Jugadores)", len(df_jugadores))

        if busqueda:
            mascara = df_jugadores.astype(str).apply(lambda row: row.str.contains(busqueda, case=False).any(), axis=1)
            df_jugadores = df_jugadores[mascara]

        st.dataframe(df_jugadores, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error al cargar la pestaña Jugadores: {e}")

# ---------------------------------------------------------
# VISTA 3: PARTIDOS
# ---------------------------------------------------------
elif menu == "Partidos":
    st.title("📅 Vista de Partidos y Predicciones")
    st.markdown("Calendario, análisis y proyecciones de los encuentros.")
    
    try:
        df_partidos = cargar_datos(URL_PARTIDOS)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Filas (Partidos)", len(df_partidos))

        if busqueda:
            mascara = df_partidos.astype(str).apply(lambda row: row.str.contains(busqueda, case=False).any(), axis=1)
            df_partidos = df_partidos[mascara]

        st.dataframe(df_partidos, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error al cargar la pestaña Partidos: {e}")
