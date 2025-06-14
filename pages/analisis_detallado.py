import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from manage_data.config_dts import ConfigDTS
# Configuración de la página
st.set_page_config(
    page_title="Análisis Detallado de Ventas",
    page_icon="📈",
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


tab1, tab2 = st.tabs(["Análisis por País", "Análisis por Método de Pago"])

with tab1:
    st.header("Análisis de Ventas por País")
    ventas_por_pais = df.groupby('pais')['venta_total'].sum().sort_values(ascending=False).reset_index()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(
            ventas_por_pais,
            x='pais',
            y='venta_total',
            title='Ventas Totales por País',
            labels={'pais': 'País', 'venta_total': 'Ventas Totales (USD)'},
            color='venta_total',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(
            xaxis_tickangle=-45,
            showlegend=False,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("Estadísticas por País:")
        st.write(ventas_por_pais)

with tab2:
    st.header("Análisis por Método de Pago")
    ventas_por_metodo = df.groupby('metodo_pago')['venta_total'].sum().sort_values(ascending=False).reset_index()
    
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(
            ventas_por_metodo,
            values='venta_total',
            names='metodo_pago',
            title='Distribución de Ventas por Método de Pago',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate="<b>%{label}</b><br>" +
                         "Ventas: $%{value:,.2f}<br>" +
                         "Porcentaje: %{percent}<extra></extra>"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("Estadísticas por Método de Pago:")
        st.write(ventas_por_metodo)

# with tab3:
#     st.header("Análisis de Satisfacción del Cliente")
    
#     col1, col2 = st.columns(2)
#     with col1:
#         fig = px.box(
#             df,
#             x='calificacion_satisfaccion',
#             y='venta_total',
#             title='Distribución de Ventas por Calificación de Satisfacción',
#             labels={
#                 'calificacion_satisfaccion': 'Calificación de Satisfacción',
#                 'venta_total': 'Venta Total (USD)'
#             },
#             color='calificacion_satisfaccion',
#             points='all'  # Muestra todos los puntos
#         )
#         fig.update_layout(
#             showlegend=False,
#             hovermode='x unified'
#         )
#         st.plotly_chart(fig, use_container_width=True)
    
#     with col2:
#         # Agregar un gráfico de dispersión adicional
#         fig2 = px.scatter(
#             df,
#             x='calificacion_satisfaccion',
#             y='venta_total',
#             color='categoria',
#             title='Relación entre Satisfacción y Ventas por Categoría',
#             labels={
#                 'calificacion_satisfaccion': 'Calificación de Satisfacción',
#                 'venta_total': 'Venta Total (USD)',
#                 'categoria': 'Categoría'
#             },
#             trendline="ols"
#         )
#         st.plotly_chart(fig2, use_container_width=True)
        
#         st.write("Estadísticas de Satisfacción:")
#         st.write(df['calificacion_satisfaccion'].describe()) 