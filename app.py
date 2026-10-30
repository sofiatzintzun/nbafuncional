import streamlit as st
import pandas as pd

# 1. Configuración general de la página
st.set_page_config(
    page_title="Mi Aplicación de Cálculos",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Panel de Control y Cálculos")
st.markdown("Bienvenido a la versión web de mi hoja de cálculo.")

# 2. Carga de datos desde Google Sheets con caché
# (Reemplaza la URL de abajo con tu enlace de Google Sheets terminado en /export?format=csv)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1RiInl1AnLDp1haLz0uMP8jsa04AppRzt8xhGSJLw7gQ/export?format=csv"

@st.cache_data(ttl=300)
def cargar_datos():
    df = pd.read_csv(SHEET_URL)
    return df

try:
    df = cargar_datos()
except Exception as e:
    st.error(f"No se pudieron cargar los datos: {e}")
    st.stop()

# 3. Mostrar datos originales
with st.expander("Ver datos sin procesar"):
    st.dataframe(df)

# 4. Resultados o métricas de ejemplo
st.subheader("Resultados")
st.dataframe(df)
