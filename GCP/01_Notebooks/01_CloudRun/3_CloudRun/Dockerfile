# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copiar dependencias primero
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la app
COPY app.py .

# Exponer el puerto para Cloud Run
EXPOSE 8080

# Comando para ejecutar la app
CMD ["python", "app.py"]
