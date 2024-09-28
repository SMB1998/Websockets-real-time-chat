# Dockerfile
FROM python:3.9-slim

# Instalar dependencias adicionales necesarias
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    libssl-dev \
    libffi-dev \
    libpq-dev \
    build-essential \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

COPY ./wait-for-it.sh /app/wait-for-it.sh

# Copiar requirements.txt y luego instalar las dependencias
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiar el resto del código del proyecto
COPY . /app

EXPOSE 8000

# Comando por defecto
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
