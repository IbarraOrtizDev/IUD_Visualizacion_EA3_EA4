import streamlit as st
import pandas as pd
import plotly.express as px

from manage_data.manage_data_city import ManageDataCity
from manage_data.config_dts import ConfigDTS

def render():
    config_dts = ConfigDTS()
    df = config_dts.get_data()

    st.title("Segmentación")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Satisfacción por Género")
        satisfaccion_genero(df)
    with col2:
        st.subheader("Distribución de Edades")
        agrupacion_edad(df)

    st.subheader("Satisfacción por Categoría")
    satisfaccion_categoria(df)

def satisfaccion_categoria(df):
    # Preparar datos
    df_cat = df[['categoria','calificacion_satisfaccion']].groupby('categoria').mean().reset_index()
    
    # Crear gráfico interactivo
    fig = px.bar(df_cat, 
                 x='categoria', 
                 y='calificacion_satisfaccion',
                 title='Satisfacción por Categoría',
                 labels={
                     'categoria': 'Categoría',
                     'calificacion_satisfaccion': 'Nivel de Satisfacción'
                 },
                 color='calificacion_satisfaccion',
                 color_continuous_scale='RdYlGn')
    
    # Personalizar diseño
    fig.update_layout(
        xaxis_tickangle=-45,
        hovermode='x unified',
        showlegend=False,
        height=500,
        template='plotly_white'
    )
    
    # Mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)

def satisfaccion_genero(df):
    # Preparar datos
    df_satisfaccion_genero = df[['genero_cliente', 'calificacion_satisfaccion']].groupby('genero_cliente').mean().reset_index()
    
    # Crear gráfico interactivo
    fig = px.bar(df_satisfaccion_genero, 
                 x='genero_cliente', 
                 y='calificacion_satisfaccion',
                 title='Satisfacción por Género',
                 labels={
                     'genero_cliente': 'Género',
                     'calificacion_satisfaccion': 'Nivel de Satisfacción'
                 },
                 color='genero_cliente',
                 color_discrete_sequence=px.colors.qualitative.Set3)
    
    # Personalizar diseño
    fig.update_layout(
        hovermode='x unified',
        showlegend=False,
        height=400,
        template='plotly_white'
    )
    
    # Añadir línea de promedio
    fig.add_hline(y=df_satisfaccion_genero['calificacion_satisfaccion'].mean(), 
                  line_dash="dash", 
                  line_color="red",
                  annotation_text="Promedio",
                  annotation_position="right")
    
    # Mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)

def agrupacion_edad(df):
    # Preparar datos
    df_age_group = df[['edad_cliente']].groupby('edad_cliente').size().reset_index(name='cantidad')
    df_age_group['rango_edad'] = df_age_group['edad_cliente'].apply(
        lambda x: '<30' if x < 30 else '30-45' if x < 45 else '>45'
    )
    df_range_age = df_age_group[['rango_edad', 'cantidad']].groupby('rango_edad').sum().reset_index()
    df_range_age = df_range_age.sort_values(by='cantidad', ascending=False)
    
    # Crear gráfico interactivo
    fig = px.bar(df_range_age, 
                 x='rango_edad', 
                 y='cantidad',
                 title='Distribución de Edades',
                 labels={
                     'rango_edad': 'Rango de Edad',
                     'cantidad': 'Cantidad de Clientes'
                 },
                 color='cantidad',
                 color_continuous_scale='Viridis')
    
    # Personalizar diseño
    fig.update_layout(
        hovermode='x unified',
        showlegend=False,
        height=400,
        template='plotly_white'
    )
    
    # Añadir porcentajes en las etiquetas
    total = df_range_age['cantidad'].sum()
    fig.update_traces(
        texttemplate='%{y} (%{customdata:.1%})',
        textposition='outside',
        customdata=[df_range_age['cantidad']/total]
    )
    
    # Mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)