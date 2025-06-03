# Sparta Gym API

API REST del sistema Sparta Gym desarrollada con Django y Django REST Framework bajo una estructura basada en Clean Architecture.

## Requisitos

- Python 3.10 o superior
- Git
- pip

## Instalación

Clona el repositorio:

```bash
git clone https://github.com/hugoberra/sparta-gym-project-test
cd sparta-gym-project-test
```

Crear y activar entorno virtual:

```bash
python -m venv env
source env/bin/activate
```

instala dependencias:

```bash
pip install -r requirements.txt
```

Aplica migraciones y corre el servidor:

```bash
python manage.py migrate
python manage.py runserver
```
