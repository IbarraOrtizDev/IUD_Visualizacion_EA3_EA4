import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from manage_data.config_dts import ConfigDTS

# Configuración de la página
st.set_page_config(
    page_title="Visualización de Ventas",
    page_icon="📊",
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
        #visualizacion-de-datos-de-ventas{
            text-align: center;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

config_dts = ConfigDTS()
df = config_dts.get_data()

st.title('Visualización de Datos de Ventas')


# Configuración de estilo para los gráficos
plt.style.use('default')  # Cambiamos a un estilo básico
sns.set_theme()  # Usamos la configuración por defecto de seaborn

## Graficos de ventas en dos columnas
col1, col2 = st.columns(2)

# 1. Gráfico de Barras: Ventas Totales por Categoría
ventas_por_categoria = df.groupby('categoria')['venta_total'].sum().sort_values(ascending=False)

with col1:
    plt.figure(figsize=(10, 6))
    sns.barplot(x=ventas_por_categoria.index, y=ventas_por_categoria.values)
    plt.title('Ventas Totales por Categoría de Producto')
    plt.xlabel('Categoría')
    plt.ylabel('Ventas Totales (USD)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.close()

# 2. Histograma: Distribución de Ventas
with col2:
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df, x='venta_total', bins=30)
    plt.title('Distribución de Ventas')
    plt.xlabel('Venta Total (USD)')
    plt.ylabel('Frecuencia')
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.close()

# 3. Gráfico de Línea: Evolución de Ventas en el Tiempo
ventas_por_fecha = df.groupby('fecha')['venta_total'].sum().reset_index()
ventas_por_fecha = ventas_por_fecha.sort_values('fecha')

plt.figure(figsize=(12, 6))
plt.plot(ventas_por_fecha['fecha'], ventas_por_fecha['venta_total'], marker='o')
plt.title('Evolución de Ventas en el Tiempo')
plt.xlabel('Fecha')
plt.ylabel('Ventas Totales (USD)')
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
st.pyplot(plt.gcf())
plt.close()

# 4. Gráfico de Dispersión: Distribución de Ventas por Categoría
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='cantidad', y='precio_unitario', hue='categoria', alpha=0.6)
plt.title('Distribución de Ventas por Categoría')
plt.xlabel('Cantidad')
plt.ylabel('Precio Unitario (USD)')
plt.legend(title='Categoría', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
st.pyplot(plt.gcf())
plt.close()
