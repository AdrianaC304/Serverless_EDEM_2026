# main.py
from flask import Flask, jsonify
from google.cloud import storage, speech, firestore
import io
import numpy as np
import soundfile as sf
import base64


app = Flask(__name__)

# Clientes de Google Cloud
storage_client = storage.Client()
speech_client = speech.SpeechClient()
firestore_client = firestore.Client()

BUCKET_NAME = 'edem-serverless-spotify-demo1'
FILE_NAME = 'podcast_audio.wav'

@app.route('/transcribeAudio', methods=['GET', 'POST'])
def transcribe_audio():
    try:
        # Descargar archivo de GCS
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(FILE_NAME)
        audio_bytes = blob.download_as_bytes()

        # Leer WAV en memoria
        audio, sr = sf.read(io.BytesIO(audio_bytes))

        # Convertir a mono
        if audio.ndim > 1:
            audio = np.mean(audio, axis=1)

        # Convertir a PCM16
        audio_pcm16 = (audio * 32767).astype(np.int16).tobytes()

        # Codificar a base64 para Speech API
        import base64
        audio_pcm16_b64 = base64.b64encode(audio_pcm16).decode("utf-8")
        audio_content = speech.RecognitionAudio(content=audio_pcm16_b64)

        # Configuración de Speech API
        audio_config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sr,
            language_code='es-ES'
        )

        # Transcripción
        response = speech_client.recognize(config=audio_config, audio=audio_content)
        transcription = ' '.join([r.alternatives[0].transcript for r in response.results])

        # Guardar en Firestore
        firestore_client.collection('transcriptions').add({
            'fileName': FILE_NAME,
            'transcription': transcription,
            'createdAt': firestore.SERVER_TIMESTAMP
        })

        return jsonify({'message': 'Transcripción guardada con .wav', 'transcription': transcription})

    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

# Entrypoint para Cloud Run
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
