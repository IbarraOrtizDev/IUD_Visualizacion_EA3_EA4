import streamlit as st
from components.tab1 import render as render_tab1
from components.tab2 import render as render_tab2
from components.tab3 import render as render_tab3

#region Configuracion de la pagina

st.set_page_config(
    page_title="ENTREGA 4",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            padding-left: 10%;
            padding-right: 10%;
            max-width: 80% !important;
        }
        #analisis-detallado-de-ventas{
            text-align: center;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

st.write("""
    <div style="text-align: center; padding-bottom: 2rem;">
        <h1>Caso de Estudio: Análisis Estratégico de ventas minoristas y comportamiento del cliente </h1>
    </div>
""", unsafe_allow_html=True)

#endregion

#region Contenido de la pagina

tab1, tab2, tab3 = st.tabs(["Análisis Descriptivo de Ventas", "Análisis de Perfil y Segmentación de Clientes", "Análisis Exploratorio de Datos y Tendencias"])

with tab1:
    render_tab1()

with tab2:
    render_tab2()

with tab3:
    render_tab3()
#endregion

