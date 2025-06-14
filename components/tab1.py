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