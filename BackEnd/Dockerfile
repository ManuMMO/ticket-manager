# Imagen base ligera
FROM python:3.12-slim

# Carpeta de trabajo dentro del contenedor
WORKDIR /app

# Instalar Poetry
RUN pip install --no-cache-dir poetry

# Copiar solo los archivos de dependencias primero (mejora la cache)
COPY pyproject.toml ./

# Instalar dependencias en el sistema del contenedor (sin virtualenv)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copiar el resto del código del backend
COPY . .

# Exponer el puerto del backend
EXPOSE 8000

# Comando de arranque del servidor Django + migraciones
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
