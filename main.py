""" 
Script: Event Driven

Description:
This function allows us to transcribe a .wav audio file into text and store
the resulting information in Firestore.

EDEM. Master Big Data & Cloud 2025/2026
Professor: Javi Briones & Adriana Campos
"""

""" Import Libraries """

import io
import numpy as np
import struct
import soundfile as sf
from google.cloud import speech, storage, firestore

# -----------------------------
# Configuration
BUCKET_NAME = "edem-serverless-spotify-demo1"
FIRESTORE_COLLECTION = "transcripciones"

speech_client = speech.SpeechClient()
storage_client = storage.Client()  
firestore_client = firestore.Client()  

def transcribe(event, context):
    """
    2nd Gen Cloud Function triggered when a file is uploaded to GCS.
    """
    file_name = event["name"]
    print(f"Processing file: {file_name}")

    # -----------------------------
    # Read WAV file from GCS
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(file_name)
    audio_data = blob.download_as_bytes()

    # -----------------------------
    # Read WAV using soundfile
    audio_array, sr = sf.read(io.BytesIO(audio_data))
    print(f"Audio loaded: {audio_array.shape} samples, Sample rate: {sr} Hz")

    # -----------------------------
    # Convert to mono if stereo
    if audio_array.ndim > 1:
        audio_array = np.mean(audio_array, axis=1)
        print(f"Converted to mono: {audio_array.shape} samples")

    # -----------------------------
    # Convert to PCM16 format
    pcm16 = b''.join(
        struct.pack('<h', int(np.clip(x * 32767, -32768, 32767)))
        for x in audio_array
    )
    print(f"Audio converted to PCM16: {len(pcm16)} bytes")

    # -----------------------------
    # Configure Speech-to-Text
    audio = speech.RecognitionAudio(content=pcm16)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sr,
        language_code="en-US",
        enable_automatic_punctuation=True
    )

    # -----------------------------
    # Transcribe audio
    response = speech_client.recognize(config=config, audio=audio)
    print("Transcription received")

    text = " ".join(
        alt.transcript
        for result in response.results
        for alt in result.alternatives
    )

    print("\n--- Transcription ---")
    print(text)
    print("---------------------")

    # -----------------------------
    # Reload blob metadata to ensure custom metadata is available
    blob.reload()
    
    metadata = blob.metadata if blob.metadata else {}
    print(f"Detected metadata: {metadata}")

    # -----------------------------
    # Store transcription and metadata in Firestore
    doc_ref = firestore_client.collection(FIRESTORE_COLLECTION).document(file_name)
    
    data_to_store = {
        "archivo": file_name,
        "transcripcion": text,
        "title": metadata.get("title"),
        "show_id": metadata.get("show_id"),
        "episode_id": metadata.get("episode_id"),
        "duration": metadata.get("duration"),
        "status": metadata.get("status")
    }
    
    doc_ref.set(data_to_store)

    print(
        f"Transcription and metadata successfully stored in Firestore "
        f"in the '{FIRESTORE_COLLECTION}' collection"
    )
