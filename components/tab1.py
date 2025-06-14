import streamlit as st
import random
import pandas as pd
import pydeck as pdk
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

from manage_data.manage_data_city import ManageDataCity
from manage_data.config_dts import ConfigDTS

def generate_random_color_rgba(alpha=160):
    return [random.randint(0, 255) for _ in range(3)] + [alpha]

def get_colors(df_group):
    colors = []
    for i in range(len(df_group)):
        colors.append(generate_random_color_rgba())
    return colors

def render():
    manage_data_city = ManageDataCity()
    config_dts = ConfigDTS()

    st.title("Gráfico de Barras Apiladas")
    st.write("Ventas por categoría desglosado por método de pago")
    df = config_dts.get_data()
    df_grouped_category_payment = df[['categoria', 'metodo_pago']].groupby(['categoria', 'metodo_pago']).size().reset_index(name='conteo')
    # Crear el gráfico interactivo con Plotly
    fig = px.bar(df_grouped_category_payment, 
                x='categoria', 
                y='conteo', 
                color='metodo_pago',
                title='Ventas por categoría desglosado por método de pago',
                labels={
                    'categoria': 'Categoría',
                    'conteo': 'Conteo',
                    'metodo_pago': 'Método de Pago'
                },
                barmode='group',
                template='plotly_white') 

    # Mostrar en Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Nuevo gráfico: Método de pago preferido por país
    st.subheader("Método de Pago Preferido por País")
    
    # Preparar datos para el nuevo gráfico
    df_pais_metodo = df[['pais', 'metodo_pago']].groupby(['pais', 'metodo_pago']).size().reset_index(name='conteo')
    
    # Calcular el total por país para obtener porcentajes
    df_pais_total = df_pais_metodo.groupby('pais')['conteo'].sum().reset_index(name='total')
    df_pais_metodo = df_pais_metodo.merge(df_pais_total, on='pais')
    df_pais_metodo['porcentaje'] = (df_pais_metodo['conteo'] / df_pais_metodo['total'] * 100).round(1)
    
    # Crear el gráfico de barras apiladas
    fig_pais = px.bar(df_pais_metodo, 
                     x='pais', 
                     y='conteo',
                     color='metodo_pago',
                     title='Distribución de Métodos de Pago por País',
                     labels={
                         'pais': 'País',
                         'conteo': 'Número de Transacciones',
                         'metodo_pago': 'Método de Pago',
                         'porcentaje': 'Porcentaje'
                     },
                     barmode='stack',
                     template='plotly_white',
                     hover_data=['porcentaje'])
    
    # Personalizar el diseño
    fig_pais.update_layout(
        xaxis_tickangle=-45,
        hovermode='x unified',
        height=500,
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    # Personalizar tooltips
    fig_pais.update_traces(
        hovertemplate="<b>País:</b> %{x}<br>" +
                     "<b>Método de Pago:</b> %{customdata[0]}<br>" +
                     "<b>Transacciones:</b> %{y}<br>" +
                     "<b>Porcentaje:</b> %{customdata[1]}%<extra></extra>",
        customdata=df_pais_metodo[['metodo_pago', 'porcentaje']].values
    )
    
    # Mostrar el gráfico
    st.plotly_chart(fig_pais, use_container_width=True)
    
    # Mostrar tabla de datos
    with st.expander("Ver datos detallados"):
        st.dataframe(
            df_pais_metodo.pivot_table(
                index='pais',
                columns='metodo_pago',
                values=['conteo', 'porcentaje'],
                aggfunc='first'
            ).round(1)
        )

    df_join = manage_data_city.df_merge_all()

    df_pais = df_join[['pais', 'venta_total']].groupby('pais').sum().reset_index()
    # Reemplazar Perú por Peru
    df_pais['pais'] = df_pais['pais'].str.replace('Perú', 'Peru')
    # Reemplazar España por Spain
    df_pais['pais'] = df_pais['pais'].str.replace('España', 'Spain')
    # Reemplazar España por Spain
    df_pais['pais'] = df_pais['pais'].str.replace('México', 'Mexico')

    
    st.title("Mapa de Ventas")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Mapa Coroplético de Ventas por País")
        fig = px.choropleth(
            df_pais,
            locations="pais",
            locationmode="country names",
            color="venta_total",
            hover_name="pais",
            projection="natural earth"
        )
        st.plotly_chart(fig)

    with col2:
        df_group = df_join[['city', 'lat', 'lng', 'venta_total']].groupby(['city', 'lat', 'lng']).sum().reset_index()

        df_mapa = pd.DataFrame({
            'lat': df_group['lat'],
            'lon': df_group['lng'],
            'info': df_group['city'],
            'radius': df_group['venta_total'],
            'color': get_colors(df_group)
        })

        st.write("Mapa de Burbujas de Ventas por Ciudad")
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=df_mapa,
            get_position='[lon, lat]',
            get_color='color',
            get_radius='radius',
        )

        view_state = pdk.ViewState(
            latitude=df_mapa['lat'].mean(),
            longitude=df_mapa['lon'].mean(),
            zoom=2,
            pitch=0,
        )

        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))