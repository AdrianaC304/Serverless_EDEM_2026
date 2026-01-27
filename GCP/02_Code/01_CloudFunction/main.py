import io
import numpy as np
import soundfile as sf
from google.cloud import firestore, speech
from apache_beam.io.filesystems import FileSystems

BUCKET_NAME = 'edem-serverless-spotify-demo1'
FIRESTORE_COLLECTION = "transcripciones"

def transcribe_audio(event, context):
    file_path = f"gs://{BUCKET_NAME}/{event['name']}"
    # Leer y normalizar audio
    with FileSystems.open(file_path) as f:
        data = f.read()
    audio_array, sr = sf.read(io.BytesIO(data))
    if audio_array.ndim > 1:
        audio_array = np.mean(audio_array, axis=1)
    
    # Convertir a bytes PCM16
    import struct
    pcm16 = b''.join(struct.pack('<h', int(x * 32767)) for x in audio_array)

    # Inicializar clientes
    firestore_client = firestore.Client()
    speech_client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=pcm16)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sr,
        language_code="es-ES",
        enable_automatic_punctuation=True
    )

    response = speech_client.recognize(config=config, audio=audio)

    texto_transcrito = " ".join(
        alt.transcript for result in response.results for alt in result.alternatives
    ).strip()

    # Guardar en Firestore
    doc_ref = firestore_client.collection(FIRESTORE_COLLECTION).document(event['name'])
    doc_ref.set({
        "archivo": event['name'],
        "transcripcion": texto_transcrito
    })

    print(f"Transcripción de {event['name']} guardada en Firestore.")
