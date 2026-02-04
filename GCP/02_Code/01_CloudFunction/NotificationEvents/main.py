"""
Cloud Function to process Pub/Sub messages.
  
    1. Receives a Pub/Sub event triggered by a message published to a Pub/Sub topic.
    2. Read the Pub/Sub messages
        - user_id
        - type
        - episode_id
    3. Processes only CONTINUE_LISTENING messages.
    4. Reads the user’s preferred language from Firestore.
    5. Read the Notification collection in Firestore to select the name.
    6. Selects the correct language template. Note that it is in lowercase.
    7. Replaces template placeholders ({{user_id}}, {{episode_id}}) with real values.
    8. Displays the message in the user's language.

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

