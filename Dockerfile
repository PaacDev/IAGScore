# Usar la imagen base de Python 3.11 slim
FROM python:3.11-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema (incluyendo Node.js para Tailwind)
RUN apt-get update && apt-get install -y --no-install-recommends \
libpq-dev \
curl \
&& curl --proto '=https' --tlsv1.2 -sSf -L https://deb.nodesource.com/setup_18.x | bash - \
&& apt-get install -y --no-install-recommends nodejs \
&& rm -rf /var/lib/apt/lists/*

# Copiar el archivo package.json de Tailwind
COPY tailwind/package.json /app/tailwind/package.json

# Instalar las dependencias de npm
# Crear un grupo y usuario no root para ejecutar los servicios
# Crea el directorio para los archivos estáticos
RUN npm install --ignore-scripts --prefix /app/tailwind \
&& groupadd -r dj_admin && useradd -r -g dj_admin dj_admin \
&& mkdir -p /app/media 

# Copiar el archivo requirements.txt e instalar dependencias de Python
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Asegurarse de que el usuario creado tenga acceso a los archivos app/media
RUN chown -R dj_admin:dj_admin /app/media

# Exponer el puerto que usará Django
EXPOSE 8000

# Copiar el archivo entrypoint.sh al contenedor
COPY entrypoint.sh /entrypoint.sh

# Establecer permisos de ejecución
RUN chmod +x /entrypoint.sh

# Establecer el entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Cambiar al usuario no root
USER dj_admin

# Comando por para ejecutar el servidor de desarrollo de Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
