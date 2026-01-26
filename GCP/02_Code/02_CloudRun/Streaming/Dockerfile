# Imagen base
FROM python:3.11-slim

# Directorio de trabajo
WORKDIR /app

# Copiar archivos
COPY requirements.txt .
COPY main.py .

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Puerto que Cloud Run espera
EXPOSE 8080

# Ejecutar Flask
CMD ["python", "main.py"]
