import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from manage_data.config_dts import ConfigDTS

def render():
    config_dts = ConfigDTS()
    df = config_dts.get_data()

    st.title("Análisis Exploratorio de Datos y Tendencias")

    grafico_evolucion_satisfaccion(df)

    col1, col2 = st.columns(2)
    with col1:
        grafico_calor(df)
    with col2:
        grafico_precio_categoria(df)

def grafico_evolucion_satisfaccion(df):
    # Preparar datos
    df_satisfaccion = df[['fecha', 'calificacion_satisfaccion']]
    df_satisfaccion['fecha'] = pd.to_datetime(df_satisfaccion['fecha']).dt.date
    df_satisfaccion = df_satisfaccion.groupby('fecha').agg({
        'calificacion_satisfaccion': ['mean', 'std', 'count']
    }).reset_index()
    df_satisfaccion.columns = ['fecha', 'media', 'std', 'count']

    # Crear gráfico interactivo
    fig = go.Figure()

    # Añadir línea principal
    fig.add_trace(go.Scatter(
        x=df_satisfaccion['fecha'],
        y=df_satisfaccion['media'],
        mode='lines+markers',
        name='Satisfacción Media',
        line=dict(color='#1f77b4', width=2),
        hovertemplate="Fecha: %{x}<br>Satisfacción: %{y:.2f}<br>Número de registros: %{customdata}<extra></extra>",
        customdata=df_satisfaccion['count']
    ))

    # Añadir banda de error
    fig.add_trace(go.Scatter(
        x=df_satisfaccion['fecha'],
        y=df_satisfaccion['media'] + df_satisfaccion['std'],
        mode='lines',
        line=dict(width=0),
        showlegend=False,
        hoverinfo='skip'
    ))

    fig.add_trace(go.Scatter(
        x=df_satisfaccion['fecha'],
        y=df_satisfaccion['media'] - df_satisfaccion['std'],
        mode='lines',
        line=dict(width=0),
        fill='tonexty',
        fillcolor='rgba(31, 119, 180, 0.1)',
        name='Desviación Estándar',
        hoverinfo='skip'
    ))

    # Personalizar diseño
    fig.update_layout(
        title='Evolución de la Satisfacción del Cliente a lo Largo del Tiempo',
        xaxis_title='Fecha',
        yaxis_title='Nivel de Satisfacción',
        hovermode='x unified',
        template='plotly_white',
        height=500,
        showlegend=True,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )

    # Mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)

def grafico_calor(df):
    # Calcular matriz de correlación
    correlation_matrix = df[['edad_cliente', 'calificacion_satisfaccion', 'cantidad']].corr()
    
    # Crear heatmap interactivo
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=correlation_matrix.round(2),
        texttemplate='%{text}',
        textfont={"size": 14},
        hoverongaps=False,
        hovertemplate='Correlación entre %{x} y %{y}: %{z:.2f}<extra></extra>'
    ))

    # Personalizar diseño
    fig.update_layout(
        title='Matriz de Correlación',
        xaxis=dict(
            tickangle=45,
            tickfont=dict(size=12)
        ),
        yaxis=dict(
            tickfont=dict(size=12)
        ),
        height=400,
        template='plotly_white',
        margin=dict(l=50, r=50, t=80, b=100)
    )

    # Mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)

def grafico_precio_categoria(df):
    # Crear gráfico de cajas interactivo
    fig = px.box(df, 
                 x='categoria', 
                 y='venta_total',
                 title='Distribución de Ventas por Categoría',
                 labels={
                     'categoria': 'Categoría',
                     'venta_total': 'Venta Total ($)'
                 },
                 color='categoria',
                 points='all',  # Muestra todos los puntos
                 template='plotly_white')

    # Personalizar diseño
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        height=400,
        hovermode='x unified'
    )

    # Añadir línea de promedio global
    fig.add_hline(y=df['venta_total'].mean(), 
                  line_dash="dash", 
                  line_color="red",
                  annotation_text="Promedio Global",
                  annotation_position="right")

    # Personalizar tooltips
    fig.update_traces(
        hovertemplate="<b>Categoría:</b> %{x}<br>" +
                     "<b>Venta:</b> $%{y:,.2f}<br>" +
                     "<extra></extra>"
    )

    # Mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)