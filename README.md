# 📋 Mini Gestor de Incidencias (Tickets)

Aplicación sencilla de gestión de incidencias con **Django + Django REST Framework** en el backend y **Nuxt 4** en el frontend.  
Todo se levanta con un solo comando usando **Docker Compose**.

# 🚀 Arranque del proyecto
Desde la raíz del repositorio:  

```bash
docker compose up
```

Esto levanta:

- Backend (Django + DRF + BBDD Sqlite)
- Frontend (Nuxt 4)

## 🔗 URLs de los servicios

**Backend (Django + DRF + BBDD Sqlite):**

- **GET / POST** → Listado y creación de tickets  
  http://localhost:8000/api/tickets/

  **Parámetros de filtrado:**  
  - `status`: `open`, `closed`, `in_progress`  
  - `priority`: `low`, `medium`, `high`

- **GET** → Estadísticas de tickets  
  http://localhost:8000/api/tickets/stats/

- **PATCH** → Actualización del estado del ticket  
  http://localhost:8000/api/tickets/id/

**Frontend (Nuxt 4 + TypeScript):**  
http://localhost:3000/

## 🧠 Decisiones técnicas

- **Uso de SQLite**:  
SQLite es suficiente para el alcance del proyecto y simplifica el entorno Docker, evitando dependencias externas. Permite un arranque rápido y reproducible. En una segunda iteración, sería buena idea migrar a PostgreSQL manteniendo la misma estructura de modelos.

- **Validación en el serializer**:  
Toda la lógica de negocio del ticket (creación sin estado closed y transición prohibida de tickets cerrados → abiertos) se implementa en el serializer. Esto centraliza la validación, evita duplicación en vistas y garantiza respuestas consistentes de la API. DRF convierte automáticamente los errores en respuestas 400 limpias.

- **Validación estricta de filtros en la vista**:  
Valido los filtros `status` y `priority` directamente en la vista porque es la capa que interpreta la petición HTTP y donde DRF expone `request.query_params`. Los serializers solo procesan datos del body y las URLs únicamente definen rutas, así que no pueden validar parámetros de consulta.

- **Configuración mediante variable de entorno**:    
Tanto `DJANGO_ALLOWED_HOSTS` como `API_BASE_URL` se gestionan vía variables de entorno definidas en Docker Compose. Esto evita hardcodear hosts o URLs, permite que los contenedores se comuniquen correctamente y facilita despliegues en distintos entornos sin modificar el código.

- **Contenedores orientados a reproducibilidad**:  
El backend pasó de un entorno con bind mount a un despliegue basado en imagen para asegurar que las dependencias se instalan dentro del contenedor. El frontend sigue la misma estrategia por los requisitos de Nuxt. Además, `.dockerignore` excluye `node_modules` para evitar copiar dependencias locales incompatibles y reducir el contexto de build.

- **Uso de composable y tipado para acceso a la API**:  
Centraliza la lógica de la API en el composable `useTickets.ts` en lugar de usar `useFetch` directamente en los componentes. Esto evita duplicación de código, mantiene la UI limpia y permite aplicar tipado y manejo de errores de forma consistente en un único punto.

## 🔄 Segunda iteración

- **Migración a PostgreSQL en Docker**:  
Sustituir SQLite por PostgreSQL para mejorar concurrencia, integridad y escalabilidad. La estructura de modelos ya es compatible, así que el cambio sería transparente para la API.

- **Paginación y ordenación avanzada en el listado**:  
Mejoraría la experiencia en listados grandes añadiendo paginación y opciones de ordenación. Esto haría la aplicación más fluida y escalable cuando aumente el número de tickets.

- **Documentación automática de la API con OpenAPI/Swagger**:  
Incorporaría documentación generada automáticamente para facilitar el uso de la API y mejorar la comunicación.

- **Autenticación básica**:  
Añadiría autenticación mínima para preparar la aplicación para escenarios multiusuario y permitir permisos diferenciados.

## 🧪 Tests

El backend incluye dos tests que validan las reglas de negocio más críticas del sistema:

- **Validación de creación** — comprueba que un ticket no puede crearse directamente con el estado `closed`.
- **Validación de transición** — verifica que un ticket en estado `closed` no puede volver a `open` sin pasar por `in_progress`.

Ambos tests garantizan la coherencia del flujo de estados y evitan inconsistencias en la API.

### ▶️ Cómo ejecutar los tests

```bash
docker exec -it backend pytest
```