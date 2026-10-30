import streamlit as st
import pandas as pd

# Configuración general de la página (Icono cambiado a balón de básquetbol)
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
# VISTA 1: EQUIPOS
# ---------------------------------------------------------
if menu == "Equipos":
    st.title("🏆 Vista de Equipos")
    st.markdown("Estadísticas y métricas generales de los equipos.")
    
    try:
        df_equipos = cargar_datos(URL_EQUIPOS)
        
        # Filtrar la columna G (índice 6) para mostrar solo los que sean diferentes a "No Juega Hoy"
        if len(df_equipos.columns) > 6:
            col_g = df_equipos.columns[6]
            df_equipos = df_equipos[df_equipos[col_g].astype(str).str.strip().str.lower() != "no juega hoy"]
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Filas (Equipos)", len(df_equipos))
        
        if busqueda:
            mascara = df_equipos.astype(str).apply(lambda row: row.str.contains(busqueda, case=False).any(), axis=1)
            df_equipos = df_equipos[mascara]

        # Configuración para transformar enlaces de texto en imágenes reales.
        configuracion_columnas = {
            "Imagen": st.column_config.ImageColumn("Logo / Imagen", width="small")
        }

        st.dataframe(
            df_equipos, 
            use_container_width=True, 
            hide_index=True,
            column_config=configuracion_columnas
        )

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
