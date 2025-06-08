import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from manage_data.config_dts import ConfigDTS

# Configuración de la página
st.set_page_config(
    page_title="Visualización de Ventas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuración de tema para Plotly
px.defaults.template = "plotly_white"
px.defaults.color_discrete_sequence = px.colors.qualitative.Set3

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

## Graficos de ventas en dos columnas
col1, col2 = st.columns(2)

# 1. Gráfico de Barras: Ventas Totales por Categoría
ventas_por_categoria = df.groupby('categoria')['venta_total'].sum().sort_values(ascending=False).reset_index()

with col1:
    fig = px.bar(
        ventas_por_categoria,
        x='categoria',
        y='venta_total',
        title='Ventas Totales por Categoría de Producto',
        labels={'categoria': 'Categoría', 'venta_total': 'Ventas Totales (USD)'},
        color='venta_total',
        color_continuous_scale='Viridis'
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

# 2. Histograma: Distribución de Ventas
with col2:
    fig = px.histogram(
        df,
        x='precio_unitario',
        y='cantidad',
        title='Distribución de Ventas por Precio Unitario',
        labels={'precio_unitario': 'Precio Unitario (USD)', 'count': 'Cantidad'},
        nbins=30,
        color_discrete_sequence=['#636EFA']
    )
    fig.update_layout(
        showlegend=False,
        hovermode='x unified'
    )
    st.plotly_chart(fig, use_container_width=True)

# 3. Gráfico de Línea: Evolución de Ventas en el Tiempo
ventas_por_fecha = df.groupby('fecha')['venta_total'].sum().reset_index()
ventas_por_fecha = ventas_por_fecha.sort_values('fecha')

fig = px.line(
    ventas_por_fecha,
    x='fecha',
    y='venta_total',
    title='Evolución de Ventas en el Tiempo',
    labels={'fecha': 'Fecha', 'venta_total': 'Ventas Totales (USD)'},
    markers=True
)
fig.update_layout(
    hovermode='x unified',
    xaxis=dict(
        tickangle=-45,
        showgrid=True
    ),
    yaxis=dict(
        showgrid=True
    )
)
st.plotly_chart(fig, use_container_width=True)

# 4. Gráfico de Dispersión: Distribución de Ventas por Categoría
fig = px.scatter(
    df,
    x='cantidad',
    y='precio_unitario',
    color='categoria',
    title='Distribución de Ventas por Categoría',
    labels={
        'cantidad': 'Cantidad',
        'precio_unitario': 'Precio Unitario (USD)',
        'categoria': 'Categoría'
    },
    opacity=0.6,
    trendline="ols"  # Agrega línea de tendencia
)
fig.update_layout(
    hovermode='closest',
    legend=dict(
        title='Categoría',
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=1.05
    )
)
st.plotly_chart(fig, use_container_width=True)
