from transformers import pipeline
import numpy as np
import soundfile as sf
import io
from flask import Flask, jsonify
from google.cloud import storage, firestore
import os

app = Flask(__name__)
storage_client = storage.Client()
firestore_client = firestore.Client()

# Inicializamos modelo como None para lazy loading
whisper_model = None

BUCKET_NAME = 'edem-serverless-spotify-demo1'
FILE_NAME = 'podcast_audio.wav'

# Función para cargar modelo solo una vez
def get_whisper_model():
    global whisper_model
    if whisper_model is None:
        whisper_model = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-small",
            framework="pt"
        )
    return whisper_model

@app.route('/transcribeAudio', methods=['POST'])
def transcribe_audio():
    try:
        model = get_whisper_model()  # carga el modelo la primera vez

        # Descargar audio desde GCS
        blob = storage_client.bucket(BUCKET_NAME).blob(FILE_NAME)
        audio_bytes = blob.download_as_bytes()

        # Leer WAV en memoria
        audio, sr = sf.read(io.BytesIO(audio_bytes))
        if audio.ndim > 1:
            audio = np.mean(audio, axis=1)  # convertir a mono

        # Transcripción directa (audio corto)
        result = model(audio)
        transcription = result["text"]

        # Guardar en Firestore
        firestore_client.collection("transcriptions").add({
            "fileName": FILE_NAME,
            "transcription": transcription,
            "createdAt": firestore.SERVER_TIMESTAMP
        })

        return jsonify({"message": "Transcripción guardada correctamente", "transcription": transcription})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Entrypoint para Cloud Run
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
