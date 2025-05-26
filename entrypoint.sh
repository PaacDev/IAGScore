#!/bin/bash

if [[ "$@" == *"celery"* ]]; then
    echo "Entrypoint detectó ejecución de Celery. Saltando setup de Django."

else

    # Ejecutar migraciones
    echo "Ejecutandp migraciones..."
    python manage.py makemigrations
    python manage.py migrate --noinput

    echo "Compilando archivos de traducción..."
    python manage.py compilemessages  > /dev/null
    echo "Compilación de traducción completada."

fi
# Iniciar el servidor de Django
exec "$@"
