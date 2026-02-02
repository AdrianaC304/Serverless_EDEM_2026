# dashboard_playback.py

import streamlit as st
from google.cloud import bigquery
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

# Configura cliente de BigQuery
client = bigquery.Client()

# Configura la página de Streamlit
st.set_page_config(page_title="Dashboard Playback", layout="wide")

# Sidebar para navegación
with st.sidebar:
    selected_page = option_menu(
        menu_title="Navegación",
        options=["KPIs", "Episodios por Usuario", "Estadísticas Avanzadas"],
        icons=["bar-chart-line", "table", "globe"],
        menu_icon="cast",
        default_index=0,
    )

# =========================
# Página 1: KPIs Generales
# =========================
if selected_page == "KPIs":
    st.title("KPIs Playback")

    # Queries
    query_episodes = """
    SELECT COUNT(DISTINCT episode_id) AS total_episodes
    FROM `serverless-477916.serverless.playback`
    """
    query_users = """
    SELECT COUNT(DISTINCT user_id) AS total_users
    FROM `serverless-477916.serverless.playback`
    """

    # Ejecuta queries
    episodes_df = client.query(query_episodes).to_dataframe()
    users_df = client.query(query_users).to_dataframe()

    # Muestra KPIs con columnas
    col1, col2 = st.columns(2)
    col1.metric("Total Episodes", episodes_df['total_episodes'][0])
    col2.metric("Total Users", users_df['total_users'][0])

# =================================
# Página 2: Episodios por Usuario
# =================================
elif selected_page == "Episodios por Usuario":
    st.title("Episodios por Usuario")

    # Query
    query_user_episodes = """
    SELECT user_id, episode_id, COUNT(*) AS plays
    FROM `serverless-477916.serverless.playback`
    GROUP BY user_id, episode_id
    ORDER BY user_id
    """
    df_user_episodes = client.query(query_user_episodes).to_dataframe()

    # Tabla interactiva
    st.dataframe(df_user_episodes)

    # Gráfico: número de episodios reproducidos por usuario
    fig = px.bar(df_user_episodes, x="user_id", y="plays", color="episode_id",
                 labels={"plays":"Reproducciones", "user_id":"Usuario", "episode_id":"Episodio"},
                 title="Reproducciones por Usuario y Episodio")
    st.plotly_chart(fig, use_container_width=True)

# =================================
# Página 3: Estadísticas Avanzadas
# =================================
elif selected_page == "Estadísticas Avanzadas":
    st.title("Estadísticas Avanzadas")

    # Query: reproducciones por país y dispositivo
    query_country_device = """
    SELECT country, device_type, COUNT(*) AS plays
    FROM `serverless-477916.serverless.playback`
    GROUP BY country, device_type
    ORDER BY plays DESC
    """
    df_country_device = client.query(query_country_device).to_dataframe()

    # Tabla
    st.dataframe(df_country_device)

    # Gráfico de calor
    fig = px.sunburst(df_country_device, path=['country', 'device_type'], values='plays',
                      title="Reproducciones por País y Tipo de Dispositivo")
    st.plotly_chart(fig, use_container_width=True)
