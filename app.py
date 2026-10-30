import streamlit as st
import pandas as pd

# Configuración general de la página
st.set_page_config(
    page_title="Panel de Análisis Deportivo",
    page_icon="⚽",
    layout="wide"
)

# Menú lateral de navegación
st.sidebar.title("Navegación")
menu = st.sidebar.radio("Selecciona una sección:", ["Equipos", "Jugadores", "Partidos"])

# URLs de cada pestaña de Google Sheets (reemplaza 'TU_ID_DE_LA_HOJA' y los 'GID')
URL_EQUIPOS = "https://docs.google.com/spreadsheets/d/1RiInl1AnLDp1haLz0uMP8jsa04AppRzt8xhGSJLw7gQ/export?format=csv&gid=0"
URL_JUGADORES = "https://docs.google.com/spreadsheets/d/1RiInl1AnLDp1haLz0uMP8jsa04AppRzt8xhGSJLw7gQ/export?format=csv&gid=417439193"
URL_PARTIDOS = "https://docs.google.com/spreadsheets/d/1RiInl1AnLDp1haLz0uMP8jsa04AppRzt8xhGSJLw7gQexport?format=csv&gid=561826503"

# Función con caché para cargar los datos de forma rápida
@st.cache_data(ttl=300)
def cargar_datos(url):
    return pd.read_csv(url)

# Lógica según la opción seleccionada en el menú lateral
if menu == "Equipos":
    st.title("🏆 Vista de Equipos")
    st.markdown("Estadísticas y métricas generales de los equipos.")
    
    try:
        df = cargar_datos(URL_EQUIPOS)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar la pestaña Equipos: {e}")

elif menu == "Jugadores":
    st.title("🏃 Vista de Jugadores")
    st.markdown("Rendimiento, uso y estadísticas individuales de los jugadores.")
    
    try:
        df = cargar_datos(URL_JUGADORES)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar la pestaña Jugadores: {e}")

elif menu == "Partidos":
    st.title("📅 Vista de Partidos y Predicciones")
    st.markdown("Calendario, análisis y proyecciones de los encuentros.")
    
    try:
        df = cargar_datos(URL_PARTIDOS)
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.error(f"Error al cargar la pestaña Partidos: {e}")
