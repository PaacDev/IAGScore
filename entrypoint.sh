#!/bin/bash

# Ejecutar migraciones
python manage.py migrate --noinput

# Iniciar el servidor de Django
exec "$@"
