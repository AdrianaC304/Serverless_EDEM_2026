"""
Notification Document Updater for Spotify Podcast Data
Generates a notification document in Firestore with multilingual messages.

EDEM. Master Big Data & Cloud 2025/2026
Professor: Javi Briones & Adriana Campos
"""

from google.cloud import firestore
import argparse
import logging

""" Input Params """

parser = argparse.ArgumentParser(description='Firestore Notification Document Updater.')

parser.add_argument('--project_id',
    required=True,
    help='GCP cloud project name.')

parser.add_argument('--firestore_collection',
    required=False,
    default='notification',
    help='Firestore collection name.')

parser.add_argument('--document_id',
    required=False,
    default='CONTINUE_LISTENING',
    help='Firestore document ID.')

args, opts = parser.parse_known_args()


def main(db, firestore_collection, document_id):
    """
    Creates or updates a notification document with multilingual messages.

    Args:
        db: Firestore client instance.
        firestore_collection: Name of the Firestore collection.
        document_id: ID of the Firestore document.
    Returns:
        None
    """

    doc_ref = db.collection(firestore_collection).document(document_id)

    payload = {
        'msg_de': "Willkommen, {{user_id}}! Schau dir Episode {{episode_id}} an",
        'msg_en': "Welcome, {{user_id}}! Take a look at episode {{episode_id}}.",
        'msg_es': "¡Bienvenido/a, {{user_id}}! Echa un vistazo al episodio {{episode_id}}.",
        'msg_fr': "Bienvenue, {{user_id}} ! Découvrez l’épisode {{episode_id}}."
    }

    try:
        doc_ref.set(payload)
        logging.info(f"Document '{document_id}' created/updated successfully in '{firestore_collection}'.")
    except Exception as e:
        logging.error(f"Error creating/updating document '{document_id}': {e}")


if __name__ == "__main__":

    # Set Logs
    logging.getLogger().setLevel(logging.INFO)

    # Run Updater
    logging.info('Initializing the notification document updater.')

    client = firestore.Client(project=args.project_id)
    main(
        db=client,
        firestore_collection=args.firestore_collection,
        document_id=args.document_id
    )
