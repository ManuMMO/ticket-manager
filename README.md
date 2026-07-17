# 📋 Mini Gestor de Incidencias (Tickets)

Aplicación sencilla de gestión de incidencias con **Django + Django REST Framework** en el backend y **Nuxt 4** en el frontend.  
Todo se levanta con un solo comando usando **Docker Compose**.

# 🚀 Arranque del proyecto
Desde la raíz del repositorio:  
[Pendiente de añadir]

Esto levanta:

- Backend (Django + DRF + BBDD Sqlite)
- Frontend (Nuxt 4)

## 🔗 URLs de los servicios

**Backend (Django + DRF):**

- **GET / POST** → Listado y creación de tickets  
  http://localhost:8000/api/tickets/

  **Parámetros de filtrado:**  
  - `status`: `open`, `closed`, `in_progress`  
  - `priority`: `low`, `medium`, `high`

- **GET** → Estadísticas de tickets  
  http://localhost:8000/api/tickets/stats/

- **PATCH** → Actualización del estado del ticket  
  http://localhost:8000/api/tickets/id/

**Frontend (Nuxt 4):**  
http://localhost:3000/

## 🧠 Decisiones técnicas

- **Uso de SQLite**:
SQLite es suficiente para el alcance del proyecto y simplifica el entorno Docker, evitando dependencias externas. Permite un arranque rápido y reproducible. En una segunda iteración, sería buena idea migrar a PostgreSQL manteniendo la misma estructura de modelos.

- **Validación en el serializer**:
Toda la lógica de negocio del ticket (creación sin estado closed y transición prohibida de tickets cerrados → abiertos) se implementa en el serializer. Esto centraliza la validación, evita duplicación en vistas y garantiza respuestas consistentes de la API. DRF convierte automáticamente los errores en respuestas 400 limpias.

- **Validación estricta de filtros en la vista**:  
Valido los filtros `status` y `priority` directamente en la vista porque es la capa que interpreta la petición HTTP y donde DRF expone `request.query_params`. Los serializers solo procesan datos del body y las URLs únicamente definen rutas, así que no pueden validar parámetros de consulta.

- **Gestión manual del campo en `update()`**:
Las validaciones ejecutadas en `update()` no forman parte del sistema de validación de campos de DRF, por lo que los errores no se asignan automáticamente. Para mantener una estructura de respuesta coherente, se fuerza explícitamente la asociación del error al campo **status**.

## 🧪 Tests

El backend incluye dos tests que validan las reglas de negocio más críticas del sistema:

- **Validación de creación** — comprueba que un ticket no puede crearse directamente con el estado `closed`.
- **Validación de transición** — verifica que un ticket en estado `closed` no puede volver a `open` sin pasar por `in_progress`.

Ambos tests garantizan la coherencia del flujo de estados y evitan inconsistencias en la API.

### ▶️ Cómo ejecutar los tests
[Pendiente de añadir]
