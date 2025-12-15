# Weather-Station-RP

Sistema de monitorización con backend Flask y frontend estático basado en la plantilla Clean Blog.

## Stack requerido
- **Backend:** Python 3 + Flask, SQLite vía SQLAlchemy, `fping` ejecutado con `subprocess`.
- **Realtime:** Server-Sent Events (SSE) para entregar mediciones en vivo.
- **Frontend:** HTML + Bootstrap 5 + JavaScript vanilla.
- **Gráficas:** Chart.js.
- **Mapa:** Leaflet.js con OpenStreetMap.
- **Persistencia:** SQLite con reportes históricos.

## Estructura del proyecto
- `/backend`: API Flask, scheduler de pings y modelo de datos.
- `/frontend`: Plantillas y archivos estáticos (HTML, CSS, JS, imágenes).
- `/docs`: Documentación y guías adicionales.

## Backend: puesta en marcha
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
python -m backend.app
```
El servicio expone:
- `GET /api/health`: estado.
- `GET /api/measurements`: últimas mediciones desde SQLite.
- `GET /api/stream`: flujo SSE con nuevos pings.

Configura hosts y frecuencia en `backend/config.py` (`FPING_TARGETS`, `FPING_INTERVAL_SECONDS`). Asegúrate de tener `fping` instalado en el sistema.

## Frontend: vista previa
Los archivos viven en `/frontend` y no requieren build. Puedes abrir `frontend/index.html` directamente o servirlos con un servidor estático:
```bash
cd frontend
python3 -m http.server 8000
```
Visita `http://localhost:8000`.

## Documentación
Consulta `/docs/ARCHITECTURE.md` para detalles de flujo de datos, endpoints y pasos de integración del frontend con SSE y Chart.js.
