# IAGScore

**IAGScore** is a platform developed for a **Final Degree Project (TFG)** that allows users to upload tasks (files) and evaluate them automatically using **language models** and artificial intelligence, based on a **custom prompt** and a **Markdown-formatted rubric** provided by the user.

---

## Main Features

- Automatic evaluation of submissions using AI  
- Free-form prompt created by the user  
- Custom rubrics in `.md` format  
- Backend Django + PostgreSQL  
- Styling with Tailwind + Flowbite  
- Asynchronous processing with Celery and Redis  
- Container deployment with Docker Compose

---

## Technologies Used

- [Django](https://www.djangoproject.com/)  
- [PostgreSQL](https://www.postgresql.org/)  
- [Ollama](https://ollama.com/)  
- [Celery](https://docs.celeryq.dev/)  
- [Redis](https://redis.io/)  
- [Docker & Docker Compose](https://docs.docker.com/)  
- [TailwindCSS](https://tailwindcss.com/) + [Flowbite](https://flowbite.com/)

---

## Prerequisites

Make sure you have installed:  
- [Git](https://git-scm.com/)  
- [Docker](https://www.docker.com/)  
- [Docker Compose](https://docs.docker.com/compose/)  
 *(included with Docker in recent versions)*

---

## Initial Setup

### 1. Clone the repository

```bash
git clone https://github.com/pac1006/IAGScore.git
cd IAGScore 
```

### 2. Create the `.env` file

Copy the example file:

**Linux and MacOS**
```bash
cp env.example .env
```
**Windows**
```powershell
copy env.example .env
```

### 3. Build with Docker Compose  
Before running this command, make sure Docker is running.  
Just open Docker Desktop and verify that it is active.

```bash
docker compose build
```

### 4. Start the project

```bash
docker compose up
```

### 5. Pull Llama3.1 Model  
Once the project is up, you must pull the model on the first run.

In another terminal, at the root of the project, IAGScore:

```bash
docker compose exec ollama ollama pull llama3.1
```
*(This step only needs to be done the first time since  
once the pull is done, the model remains in Ollama.)*

---

## Optional Setup

### 6. Create Django superuser  
Optionally, a superuser can be created to access the Django admin panel.

```bash
docker compose exec web python3 manage.py createsuperuser
```

You will need to enter:
- Email  
- Username  
- Password

---

## License

This project is licensed under the **MIT License**.

---

## Author

Developed by [Pedro Antonio Abellaneda Canales](https://github.com/pac1006).