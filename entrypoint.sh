#!/bin/bash

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate --noinput

# Iniciar el servidor de Django
exec "$@"
