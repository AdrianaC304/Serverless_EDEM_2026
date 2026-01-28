import io
import numpy as np
import struct
import soundfile as sf
from google.cloud import speech, storage, firestore

# -----------------------------
BUCKET_NAME = "edem-serverless-spotify-demo1"
FIRESTORE_COLLECTION = "transcripciones"

speech_client = speech.SpeechClient()
storage_client = storage.Client()  # Cliente para leer desde GCS
firestore_client = firestore.Client()  # Cliente para escribir en Firestore

def transcribe(event, context):
    """
    Cloud Function 2nd Gen que se dispara al subir un archivo a GCS.
    """
    file_name = event["name"]
    print(f"Procesando archivo: {file_name}")

    # -----------------------------
    # 1️⃣ Leer WAV desde GCS
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_name)
    audio_data = blob.download_as_bytes()

    audio_array, sr = sf.read(io.BytesIO(audio_data))
    print(f"Audio leído: {audio_array.shape} muestras, Frecuencia de muestreo: {sr} Hz")

    # -----------------------------
    # 2️⃣ Convertir a mono si es estéreo
    if audio_array.ndim > 1:
        audio_array = np.mean(audio_array, axis=1)
        print(f"Convertido a mono: {audio_array.shape} muestras")

    # -----------------------------
    # 3️⃣ Convertir a PCM16
    pcm16 = b''.join(
        struct.pack('<h', int(np.clip(x * 32767, -32768, 32767)))
        for x in audio_array
    )
    print(f"Audio convertido a PCM16: {len(pcm16)} bytes")

    # -----------------------------
    # 4️⃣ Configurar Speech-to-Text
    audio = speech.RecognitionAudio(content=pcm16)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sr,
        language_code="en-US",
        enable_automatic_punctuation=True
    )

    # -----------------------------
    # 5️⃣ Transcribir
    response = speech_client.recognize(config=config, audio=audio)
    print("Transcripción recibida ✅")

    # -----------------------------
    # 6️⃣ Extraer texto
    texto = " ".join(
        alt.transcript
        for result in response.results
        for alt in result.alternatives
    )

    print("\n--- Transcripción ---")
    print(texto)
    print("---------------------")

    # -----------------------------
    # 7️⃣ Guardar en Firestore
    doc_ref = firestore_client.collection(FIRESTORE_COLLECTION).document(file_name)
    doc_ref.set({
        "archivo": file_name,
        "transcripcion": texto
    })
    print(f"Transcripción guardada en Firestore en la colección '{FIRESTORE_COLLECTION}'")
