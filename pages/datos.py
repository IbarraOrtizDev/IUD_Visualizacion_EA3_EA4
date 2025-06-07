import streamlit as st
from manage_data.config_dts import ConfigDTS
# Configuración de la página
st.set_page_config(
    page_title="Análisis Detallado de Ventas",
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

st.title("Data Set")

config_dts = ConfigDTS()
df = config_dts.get_data()

st.write("Datos de Ventas:")
st.write(df)

st.write("Ventas por Categoría:")
ventas_por_categoria = df.groupby('categoria')['venta_total'].sum().sort_values(ascending=False)

st.write(ventas_por_categoria)