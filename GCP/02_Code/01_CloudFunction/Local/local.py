import io
import numpy as np
import struct
import soundfile as sf
from google.cloud import speech
from google.oauth2 import service_account

# -----------------------------
# CONFIGURACIÓN
LOCAL_WAV_FILE = "podcast_audio.wav"  # Cambia al nombre de tu WAV
LANGUAGE = "en-US"                    # Inglés
#CREDENTIALS_JSON = r"/"  # Cambia a tu JSON

# -----------------------------
# Inicializar cliente con credenciales explícitas
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_JSON)
speech_client = speech.SpeechClient(credentials=credentials)

# -----------------------------
# 1️⃣ Leer WAV
audio_array, sr = sf.read(LOCAL_WAV_FILE)
print(f"Audio leído: {audio_array.shape} muestras, Frecuencia de muestreo: {sr} Hz")

# 2️⃣ Convertir a mono si es estéreo
if audio_array.ndim > 1:
    audio_array = np.mean(audio_array, axis=1)
    print(f"Convertido a mono: {audio_array.shape} muestras")

# 3️⃣ Convertir a PCM16
pcm16 = b''.join(struct.pack('<h', int(np.clip(x * 32767, -32768, 32767))) for x in audio_array)
print(f"Audio convertido a PCM16: {len(pcm16)} bytes")

# -----------------------------
# 4️⃣ Configurar solicitud a Google Speech-to-Text
audio = speech.RecognitionAudio(content=pcm16)
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=sr,
    language_code=LANGUAGE,
    enable_automatic_punctuation=True
)

# -----------------------------
# 5️⃣ Transcribir audio
print("Enviando audio a Google Speech-to-Text...")
response = speech_client.recognize(config=config, audio=audio)
print("Transcripción recibida ✅")

# -----------------------------
# 6️⃣ Extraer y mostrar texto
texto = " ".join(
    alt.transcript
    for result in response.results
    for alt in result.alternatives
)

print("\n--- Transcripción ---")
print(texto)
print("---------------------")
