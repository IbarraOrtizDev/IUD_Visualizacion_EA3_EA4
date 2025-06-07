import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
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

st.title("Análisis Detallado de Ventas")

# Cargar datos
config_dts = ConfigDTS()
df = config_dts.get_data()

# Crear pestañas para diferentes análisis
tab1, tab2, tab3 = st.tabs(["Análisis por País", "Análisis por Método de Pago", "Análisis de Satisfacción"])

with tab1:
    st.header("Análisis de Ventas por País")
    ventas_por_pais = df.groupby('pais')['venta_total'].sum().sort_values(ascending=False)
    
    col1, col2 = st.columns(2)
    with col1:
        plt.figure(figsize=(10, 6))
        sns.barplot(x=ventas_por_pais.index, y=ventas_por_pais.values)
        plt.title('Ventas Totales por País')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt.gcf())
        plt.close()
    
    with col2:
        st.write("Estadísticas por País:")
        st.write(ventas_por_pais)

with tab2:
    st.header("Análisis por Método de Pago")
    ventas_por_metodo = df.groupby('metodo_pago')['venta_total'].sum().sort_values(ascending=False)
    
    col1, col2 = st.columns(2)
    with col1:
        plt.figure(figsize=(10, 6))
        plt.pie(ventas_por_metodo.values, labels=ventas_por_metodo.index, autopct='%1.1f%%')
        plt.title('Distribución de Ventas por Método de Pago')
        plt.tight_layout()
        st.pyplot(plt.gcf())
        plt.close()
    
    with col2:
        st.write("Estadísticas por Método de Pago:")
        st.write(ventas_por_metodo)

with tab3:
    st.header("Análisis de Satisfacción del Cliente")
    
    col1, col2 = st.columns(2)
    with col1:
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=df, x='calificacion_satisfaccion', y='venta_total')
        plt.title('Distribución de Ventas por Calificación de Satisfacción')
        plt.tight_layout()
        st.pyplot(plt.gcf())
        plt.close()
    
    with col2:
        st.write("Estadísticas de Satisfacción:")
        st.write(df['calificacion_satisfaccion'].describe()) 