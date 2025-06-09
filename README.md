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

Una vez levantado el proyecto, es necesario hacer **pull del modelo** que se desea usar en la primera ejecución.

Por ejemplo, para descargar el modelo `llama3.1`, ejecuta en otra terminal desde la raíz del proyecto (`IAGScore`):

```bash
docker compose exec ollama ollama pull llama3.1
```
*(Este paso únicamente es necesario hacerlo en la primera ejecución ya que
una vez hecho el pull, el modelo permanece en Ollama.
)*

#### Recursos del sistema y configuración

El modelo `llama3.1` requiere una cantidad significativa de recursos (RAM, CPU y posiblemente GPU).

Asegúrate de que Docker Desktop tenga suficiente memoria y CPU asignados:

- Ve a **Docker Desktop > Settings > Resources**.
- Se recomienda asignar al menos **8–12 GB de RAM** y **4 CPUs** para un rendimiento adecuado.

---

#### Otros modelos disponibles

Puedes hacer **pull de cualquier otro modelo** soportado por Ollama.

```bash
docker compose exec ollama ollama pull <nombre-del-modelo>
```

Por ejemplo:

```bash
docker compose exec ollama ollama pull mistral
```

#### Modelos cargados

Puedes consultar tus modelos cargados en Ollama

```bash
docker compose exec ollama ollama list
```

#### Eliminar modelos

Puedes eliminar un modelo cargado en Ollama ejecutando el siguiente comando

```bash
docker compose exec ollama ollama rm <nombre-del-modelo>
```

## Configuración opcional

### 6. Crea superusuario Django
Opcionalmente se puede crear un superusuario para poder acceder al panel de administración de Django

```bash
docker compose exec web python3 manage.py createsuperuser
```
Deberás introducir:
- Email
- Username
- Password

---

### 7. Carpeta `ejemplos` – Recursos de prueba

Una vez que la aplicación esté en funcionamiento y el modelo cargado, puedes utilizar los materiales incluidos en la carpeta `ejemplos` del repositorio para hacer pruebas de manera rápida:

- Un **prompt** predefinido para copiar y pegar directamente.
- Una **rúbrica en formato Markdown** lista para importar.
- Un **archivo comprimido con tareas Java** basadas en el problema de Fibonacci, útil para evaluar el funcionamiento del sistema de corrección automática.

Esta carpeta es ideal para realizar pruebas sin necesidad de crear archivos desde cero. Te permite comprobar el flujo completo.

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

