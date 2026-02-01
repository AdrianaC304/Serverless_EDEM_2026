""" 
Script: App & BI

Description:

This code reads data from BigQuery to create a Streamlit dashboard showing:  
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

# Configure BigQuery client
client = bigquery.Client()

# Set Streamlit page configuration
st.set_page_config(page_title="Dashboard Playback", layout="wide")
st.title("KPIs Playback")

# Query to count distinct episodes
query_episodes = """
SELECT COUNT(DISTINCT episode_id) AS total_episodes
FROM `serverless-477916.serverless.playback`
"""

# Query to count distinct users
query_users = """
SELECT COUNT(DISTINCT user_id) AS total_users
FROM `serverless-477916.serverless.playback`
"""

# TODO: Create visualization showing each episode associated with each user

# Execute queries
episodes_df = client.query(query_episodes).to_dataframe()
users_df = client.query(query_users).to_dataframe()

# Display KPIs
col1, col2 = st.columns(2)

col1.metric("Total Episodes", episodes_df['total_episodes'][0])
col2.metric("Total Users", users_df['total_users'][0])
