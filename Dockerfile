# Imagen base de Python
FROM python:3.12-slim

# Establece directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos
COPY . .

# Instalar dependencias
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponer el puerto donde correrá FastAPI
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

