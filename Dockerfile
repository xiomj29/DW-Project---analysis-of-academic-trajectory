# Usa Python 3.11 optimizado
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala dependencias del sistema necesarias para compilar psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala requerimientos
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia todo tu proyecto al contenedor
COPY . /app/

# Expone el puerto del backend
EXPOSE 8000

# Comando por defecto para correr el servidor con Gunicorn
CMD ["gunicorn", "dw_project.wsgi:application", "--bind", "0.0.0.0:8000"]
