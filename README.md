# IAGScore
[![Django Develop CI](https://github.com/pac1006/IAGScore/actions/workflows/django_develop.yml/badge.svg?branch=develop)](https://github.com/pac1006/IAGScore/actions/workflows/django_develop.yml)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=pac1006_IAGScore&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=pac1006_IAGScore)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=pac1006_IAGScore&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=pac1006_IAGScore)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=pac1006_IAGScore&metric=coverage)](https://sonarcloud.io/summary/new_code?id=pac1006_IAGScore)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=pac1006_IAGScore&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=pac1006_IAGScore)

**IAGScore** es una plataforma desarrollada para un **Trabajo Fin de Grado (TFG)** que permite a los usuarios subir tareas (archivos) y evaluarlas automáticamente usando **modelos de lenguaje** e inteligencia artificial, basándose en un **prompt personalizado** y una **rúbrica en formato Markdown** proporcionada por el usuario.

---

## Características principales

- Evaluación automática de entregas usando IA (Ollama)
- Prompt libre creado por el usuario
- Rúbricas personalizadas en formato `.md`
- Backend Django + PostgreSQL
- Estilos con Tailwind + Flowbite
- Procesamiento asíncrono con Celery y Redis
- Desplegado de contenedores con Docker Compose

---

## Tecnologías utilizadas

- [Django](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Ollama](https://ollama.com/)
- [Celery](https://docs.celeryq.dev/)
- [Redis](https://redis.io/)
- [Docker & Docker Compose](https://docs.docker.com/)
- [TailwindCSS](https://tailwindcss.com/) + [Flowbite](https://flowbite.com/)

---

## Requisitos previos

Asegúrate de tener instalado:
- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
 *(incluido con Docker en versiones recientes)*

---

## Configuración inicial

### 1. Clonar el repositorio

```bash
git clone https://github.com/pac1006/IAGScore.git
cd IAGScore 
```

### 2. Crea el archivo `.env`

Copia el archivo de ejemplo:

**Linux y MacOs**
```bash
cp env.example .env
```
**Windows**
```powershell
copy env.example .env
```

### 3. Build con Docker Compose
Antes de ejecutar este comando, asegúrate de que Docker esté en funcionamiento.
Basta con abrir Docker Desktop y verificar que está activo.

```bash
docker compose build
```

### 4. Levanta proyecto 

```bash
docker compose up
```

### 5. Pull Modelo Llama3.1
Levantado el proyecto, se debe de hacer Pull del modelo en la primera ejecución.

En otra terminal, en la raiz del proyecto, IAGScore

```bash
docker compose exec ollama ollama pull llama3.1
```
*(Este paso únicamente es necesario hacerlo en la primera ejecución ya que
una vez hecho el pull, el modelo permanece en Ollama.
)*
## Configuración opcional

### 6. Crea superusuario Django
Opcionalmente se puede crear un superusuario para poder acceder al panel de administracion de Django

```bash
docker compose exec web python3 manage.py createsuperuser
```
Deberás introducir:
- Email
- Username
- Password

---

## Licencia

Este proyecto está licenciado bajo la **MIT License**.  
Consulta el archivo [LICENSE](LICENSE) para más detalles.

---
## Autor

Desarrollado por [Pedro Antonio Abellaneda Canales](https://github.com/pac1006).

---
## Solución de errores

Consulta la [guía de solución de errores](./TROUBLESHOOTING.md) para ver cómo resolver problemas comunes.

