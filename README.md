# 📋 Mini Gestor de Incidencias (Tickets)

Aplicación sencilla de gestión de incidencias con **Django + Django REST Framework** en el backend y **Nuxt 4** en el frontend.  
Todo se levanta con un solo comando usando **Docker Compose**.

# 🚀 Arranque del proyecto
Desde la raíz del repositorio:
[Pendiente añadirlo]

Esto levanta:

- Backend (Django + DRF + BBDD Sqlite)
- Frontend (Nuxt 4)

## 🔗 URLs de los servicios

**Backend (Django + DRF):**  

- **GET / POST** → Listado y creación de tickets  
  http://localhost:8000/api/tickets/

- **GET** → Estadísticas de tickets  
  http://localhost:8000/api/tickets/stats/

- **PATCH** → Actualización del estado del ticket  
  http://localhost:8000/api/tickets/<id>/


**Frontend (Nuxt 4):**  
http://localhost:3000/

## 🧠 Decisiones técnicas

- Uso de SQLite
SQLite es suficiente para el alcance del proyecto y simplifica el entorno Docker, evitando dependencias externas. Permite un arranque rápido y reproducible. En una segunda iteración, sería buena idea migrar a PostgreSQL manteniendo la misma estructura de modelos.

- Validación en el serializer
Toda la lógica de negocio del ticket (creación sin estado closed y transición prohibida de tickets cerrados → abiertos) se implementa en el serializer. Esto centraliza la validación, evita duplicación en vistas y garantiza respuestas consistentes de la API. DRF convierte automáticamente los errores en respuestas 400 limpias.