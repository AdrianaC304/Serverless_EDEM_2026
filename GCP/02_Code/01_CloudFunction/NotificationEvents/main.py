"""
    Cloud Function to process Pub/Sub messages.
   1. Read the Pub/Sub messages (user_id, type and episode_id).
   2. Processes only CONTINUE_LISTENING messages.
   3. Read the lenguage for the user in Firestore.
   4. Read the notification collection in Firestore.
   5. Displays the message in the user's language.

EDEM. Master Big Data & Cloud 2025/2026
Professor: Javi Briones & Adriana Campos
"""


import base64
import json
from google.cloud import firestore

# Initialize Firestore client
firestore_client = firestore.Client()

def notification(event, context):
    """
    Gen2 Cloud Function 
    """
    #ToDo

