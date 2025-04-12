# Imagen base de Python (más compatible con el entorno del docker-compose)
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos del proyecto al directorio de trabajo
COPY . .

# Instalar las dependencias definidas en requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Definir el comando por defecto para ejecutar la aplicación
CMD ["python", "src/app.py"]
