# Weather Station Architecture

## Stack
- **Backend:** Python 3 + Flask, SQLite (SQLAlchemy), fping integration via subprocess, Server-Sent Events (SSE) for tiempo real.
- **Frontend:** HTML, Bootstrap 5 y JavaScript vanilla.
- **Gráficas:** Chart.js.
- **Mapa:** Leaflet.js con OpenStreetMap.

## Carpetas
- `/backend`: API Flask, scheduler de pings con fping, modelo SQLite, endpoints REST + SSE.
- `/frontend`: Plantillas y estáticos (HTML, CSS, JS, imágenes).
- `/docs`: Documentación y guías.

## Flujo de datos
1. `Monitor` ejecuta `fping` periódicamente (configurable) para cada host objetivo.
2. Los resultados se persisten en SQLite a través de SQLAlchemy (`Measurement`).
3. Los eventos recientes se publican vía SSE en `/api/stream` para la UI en vivo.
4. Históricos se consultan por REST en `/api/measurements`.

## Endpoints clave
- `GET /api/health`: estado del servicio.
- `GET /api/measurements`: últimos registros (límite configurable).
- `GET /api/stream`: flujo SSE de eventos de latencia y disponibilidad.

## Configuración
Valores por defecto en `backend/config.py`:
- `FPING_TARGETS`: hosts a sondear (ej. `8.8.8.8`, `1.1.1.1`).
- `FPING_INTERVAL_SECONDS`: frecuencia de pings.
- `MAX_MEASUREMENTS`: límite de resultados para consultas rápidas.
- `SSE_RETRY_MILLISECONDS`: hint de reconexión SSE para el cliente.

## Ejecución rápida
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
El servidor escucha en `http://localhost:8000`.

## Integración Frontend
- Conecta SSE a `http://localhost:8000/api/stream` para gráficos en tiempo real con Chart.js.
- Usa `GET /api/measurements` para cargar históricos y mostrarlos en tablas o reportes.
- Leaflet.js puede consumir los datos de disponibilidad para pintar marcadores en tiempo real.
