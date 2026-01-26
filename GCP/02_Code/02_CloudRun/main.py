import streamlit as st
from google.cloud import bigquery
import pandas as pd

# Configuración de BigQuery
client = bigquery.Client()

st.set_page_config(page_title="Dashboard Playback", layout="wide")
st.title("KPIs Playback")

# Query para conteo de episodios distintos
query_episodes = """
SELECT COUNT(DISTINCT episode_id) AS total_episodes
FROM `serverless-477916.serverless.playback`
"""

# Query para conteo de usuarios distintos
query_users = """
SELECT COUNT(DISTINCT user_id) AS total_users
FROM `serverless-477916.serverless.playback`
"""

# Ejecutar queries
episodes_df = client.query(query_episodes).to_dataframe()
users_df = client.query(query_users).to_dataframe()

# Mostrar KPIs
col1, col2 = st.columns(2)

col1.metric("Total Episodes", episodes_df['total_episodes'][0])
col2.metric("Total Users", users_df['total_users'][0])
