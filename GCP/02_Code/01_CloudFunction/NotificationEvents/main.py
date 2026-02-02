import base64
import json
from google.cloud import firestore

# Inicializar cliente Firestore
firestore_client = firestore.Client()

def notification(event, context):
    """
    Función Cloud Function Gen2 para procesar mensajes Pub/Sub.
    Procesa mensajes CONTINUE_LISTENING y muestra el mensaje en el idioma del usuario.
    """
    try:
        # Pub/Sub entrega mensaje en base64
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        data = json.loads(pubsub_message)
    except Exception as e:
        print("Error parseando mensaje:", e)
        return

    msg_type = data.get("type")
    user_id = data.get("user_id")
    episode_id = data.get("payload", {}).get("episode_id")

    if msg_type != "CONTINUE_LISTENING":
        print("Tipo de mensaje ignorado:", msg_type)
        return

    if not user_id or not episode_id:
        print("Mensaje incompleto: falta user_id o episode_id")
        return

    # 1️⃣ Obtener idioma del usuario
    user_ref = firestore_client.collection("users").document(user_id)
    user_doc = user_ref.get()

    if not user_doc.exists:
        print(f"Usuario {user_id} no encontrado")
        return

    language = user_doc.to_dict().get("language", "EN")  # Por defecto EN

    # Validar que el idioma esté dentro de los esperados
    valid_languages = ['EN', 'ES', 'DE', 'FR']
    if language.upper() not in valid_languages:
        print(f"Idioma {language} no válido, usando EN por defecto")
        language = 'EN'

    # 2️⃣ Obtener mensaje de notifications
    notif_ref = firestore_client.collection("notifications").document("CONTINUE_LISTENING")
    notif_doc = notif_ref.get()

    if not notif_doc.exists:
        print("Documento de notificaciones no encontrado")
        return

    notif_data = notif_doc.to_dict()
    msg_key = f"msg_{language.lower()}"  # minúsculas para Firestore

    template = notif_data.get(msg_key)
    if not template:
        print(f"No existe mensaje para el idioma {language}, usando EN por defecto")
        template = notif_data.get("msg_en")  # fallback al inglés

        if not template:
            print("No existe mensaje en inglés tampoco. Revisar Firestore.")
            return

    # 3️⃣ Reemplazar variables
    final_message = template.replace("{{user_id}}", user_id).replace("{{episode_id}}", episode_id)

    # Mostrar mensaje final
    print(final_message)
