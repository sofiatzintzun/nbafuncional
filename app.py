import streamlit as st
import pandas as pd

# 1. Configuración general de la página
st.set_page_config(
    page_title="Panel de Análisis Deportivo",
    page_icon="🏀",
    layout="wide"
)

# 2. Inyección de CSS con opacidad controlada para la imagen de fondo
BG_IMAGE_URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTZAtzM_7vjNgkwvj0lA-Y94T4lwnyb5yE0Lr9u1p-IdayCQczuvhXOns4&s=10"

st.markdown(
    f"""
    <style>
    .stApp::before {{
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("{BG_IMAGE_URL}");
        background-attachment: fixed;
        background-size: cover;
        opacity: 0.3;
        z-index: -1;
    }}
    </style>
    """,
    unsafe_allow_html=True
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
        
        if len(df_equipos.columns) > 6:
            col_g = df_equipos.columns[6]
            df_equipos = df_equipos[df_equipos[col_g].astype(str).str.strip().str.lower() != "no juega hoy"]
        
        if busqueda:
            mascara = df_equipos.astype(str).apply(lambda row: row.str.contains(busqueda, case=False).any(), axis=1)
            df_equipos = df_equipos[mascara]

        st.metric("Equipos Mostrados", len(df_equipos))
        st.markdown("---")

        for index, row in df_equipos.iterrows():
            with st.container(border=True):
                col_img, col_info = st.columns([1, 4])
                
                with col_img:
                    try:
                        imagen_url = row.iloc[9]
                        if pd.notna(imagen_url) and str(imagen_url).startswith("http"):
                            st.image(imagen_url, width=100)
                        else:
                            st.write("🏀")
                    except:
                        st.write("🏀")

                with col_info:
                    nombre_equipo = row.iloc[1] if len(row) > 1 else "Equipo"
                    st.subheader(f"{nombre_equipo}")
                    
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
# VISTA 2: JUGADORES (Diseño basado en tu boceto)
# ---------------------------------------------------------
elif menu == "Jugadores":
    st.title("🏃 Vista de Jugadores")
    st.markdown("Rendimiento, uso y estadísticas individuales de los jugadores.")
    
    try:
        df_jugadores = cargar_datos(URL_JUGADORES)
        df_jugadores = df_jugadores.fillna("")
        
        # Filtrar para mostrar solo los que tienen algo escrito en la Columna A (índice 0)
        if len(df_jugadores.columns) > 0:
            col_a = df_jugadores.columns[0]
            df_jugadores = df_jugadores[
                (df_jugadores[col_a].astype(str).str.strip() != "") & 
                (df_jugadores[col_a].astype(str).str.lower() != "nan") &
                (df_jugadores[col_a].astype(str).str.lower() != "none")
            ]
        
        if busqueda:
            mascara = df_jugadores.astype(str).apply(lambda row: row.str.contains(busqueda, case=False).any(), axis=1)
            df_jugadores = df_jugadores[mascara]

        st.metric("Jugadores Mostrados", len(df_jugadores))
        st.markdown("---")

        # Iterar sobre cada fila para crear las tarjetas según el boceto de Jugadores:
        for index, row in df_jugadores.iterrows():
            with st.container(border=True):
                col_img, col_enf = st.columns([1, 4])
                
                with col_img:
                    try:
                        imagen_url = row.iloc[9] if len(row) > 9 else "" # Columna J (índice 9)
                        if pd.notna(imagen_url) and str(imagen_url).startswith("http"):
                            st.image(imagen_url, width=100)
                        else:
                            st.write("🏀")
                    except:
                        st.write("🏀")

                with col_enf:
                    col_a_val = row.iloc[0] if len(row) > 0 else ""
                    st.subheader(f"📌 {col_a_val}")

                st.markdown("---")

                # Columnas inferiores: Izquierda (B, D, F) vs Derecha (C, E, G)
                col_izq, col_der = st.columns(2)

                with col_izq:
                    try:
                        b_val = row.iloc[1] if len(row) > 1 else ""
                        d_val = row.iloc[3] if len(row) > 3 else ""
                        f_val = row.iloc[5] if len(row) > 5 else ""
                        
                        col_b_name = df_jugadores.columns[1] if len(df_jugadores.columns) > 1 else "B"
                        col_d_name = df_jugadores.columns[3] if len(df_jugadores.columns) > 3 else "D"
                        col_f_name = df_jugadores.columns[5] if len(df_jugadores.columns) > 5 else "F"

                        st.metric(label=str(col_b_name), value=str(b_val))
                        st.markdown(f"**{col_d_name}:** {d_val}")
                        st.markdown(f"**{col_f_name}:** {f_val}")
                    except Exception as e:
                        st.text("Datos no disponibles")

                with col_der:
                    try:
                        c_val = row.iloc[2] if len(row) > 2 else ""
                        e_val = row.iloc[4] if len(row) > 4 else ""
                        g_val = row.iloc[6] if len(row) > 6 else ""
                        
                        col_c_name = df_jugadores.columns[2] if len(df_jugadores.columns) > 2 else "C"
                        col_e_name = df_jugadores.columns[4] if len(df_jugadores.columns) > 4 else "E"
                        col_g_name = df_jugadores.columns[6] if len(df_jugadores.columns) > 6 else "G"

                        st.metric(label=str(col_c_name), value=str(c_val))
                        st.markdown(f"**{col_e_name}:** {e_val}")
                        st.markdown(f"**{col_g_name}:** {g_val}")
                    except Exception as e:
                        st.text("Datos no disponibles")

    except Exception as e:
        st.error(f"Error al cargar la pestaña Jugadores: {e}")

# ---------------------------------------------------------
# VISTA 3: PARTIDOS (Formato de tabla limpia)
# ---------------------------------------------------------
elif menu == "Partidos":
    st.title("📅 Vista de Partidos y Predicciones")
    st.markdown("Calendario, análisis y proyecciones de los encuentros.")
    
    try:
        df_partidos = cargar_datos(URL_PARTIDOS)
        df_partidos = df_partidos.fillna("")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total de Filas (Partidos)", len(df_partidos))

        if busqueda:
            mascara = df_partidos.astype(str).apply(lambda row: row.str.contains(busqueda, case=False).any(), axis=1)
            df_partidos = df_partidos[mascara]

        st.dataframe(df_partidos, use_container_width=True, hide_index=True)

    except Exception as e:
        st.error(f"Error al cargar la pestaña Partidos: {e}")
