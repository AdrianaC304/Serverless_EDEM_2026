""" 
Script: App & BI

Description:

This code allows us to read data from BigQuery to create a Streamlit dashboard showing:  
- The total number of episodes in the database  
- The total number of users in the database  
- Each episode associated with each user


EDEM. Master Big Data & Cloud 2025/2026
Professor: Javi Briones & Adriana Campos
"""

""" Import Libraries """

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

# ToDo - Graphic with each episode associated with each user in 
# ToDo 
# ToDo 

# Ejecutar queries
episodes_df = client.query(query_episodes).to_dataframe()
users_df = client.query(query_users).to_dataframe()

# Mostrar KPIs
col1, col2 = st.columns(2)

col1.metric("Total Episodes", episodes_df['total_episodes'][0])
col2.metric("Total Users", users_df['total_users'][0])
