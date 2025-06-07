import pydeck as pdk
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import random
from manage_data.config_dts import ConfigDTS
from manage_data.manage_data_city import ManageDataCity
def generate_random_color_rgba(alpha=160):
    return [random.randint(0, 255) for _ in range(3)] + [alpha]

def get_colors(df_group):
    colors = []
    for i in range(len(df_group)):
        colors.append(generate_random_color_rgba())
    return colors

config_dts = ConfigDTS()
df = config_dts.get_data()
manage_data_city = ManageDataCity()
df_join = manage_data_city.merge_data(df)
df_group = df_join[['city', 'lat', 'lng', 'venta_total']].groupby(['city', 'lat', 'lng']).sum().reset_index()

df_mapa = pd.DataFrame({
    'lat': df_group['lat'],
    'lon': df_group['lng'],
    'info': df_group['city'],
    'radius': df_group['venta_total'],
    'color': get_colors(df_group)
})

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

st.title("Mapa de Ventas")

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
    zoom=3,
    pitch=0,
)

st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

st.write("Datos del mapa")
st.write(df_group)

