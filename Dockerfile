# Usar la imagen base de Python 3.11 slim
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema (incluyendo Node.js para Tailwind)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Verificar la instalación de node y npm (esto es opcional pero útil para la depuración)
RUN node -v && npm -v

# Copiar el archivo package.json de Tailwind y luego instalar las dependencias de npm
COPY tailwind/package.json /app/tailwind/package.json

RUN npm install --prefix /app/tailwind
RUN mkdir -p /app/media && chmod -R 777 /app/media

# Copiar el archivo requirements.txt e instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Crear un grupo y usuario no root para ejecutar los servicios
RUN groupadd -r dj_admin && useradd -r -g dj_admin dj_admin

# Asegurarse de que el usuario creado tenga acceso a los archivos de la app
RUN chown -R dj_admin:dj_admin /app

# Exponer el puerto que usará Django
EXPOSE 8000

# Copiar el archivo entrypoint.sh al contenedor
COPY entrypoint.sh /entrypoint.sh

# Establecer permisos de ejecución
RUN chmod +x /entrypoint.sh

# Establecer el entrypoint
ENTRYPOINT ["/entrypoint.sh"]
RUN chgrp -R dj_admin /app
RUN chmod -R g+w /app
# Cambiar la propiedad de la carpeta media a celery
RUN chown -R dj_admin:dj_admin /app/media

USER dj_admin

# Comando por defecto (se sobrescribirá en docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
