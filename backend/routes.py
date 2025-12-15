import json
from flask import Blueprint, Response, current_app, jsonify

bp = Blueprint("api", __name__)


@bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@bp.route("/measurements", methods=["GET"])
def measurements():
    monitor = current_app.extensions["monitor"]
    limit = current_app.config.get("MAX_MEASUREMENTS", 200)
    return jsonify(monitor.recent_events(limit))


@bp.route("/stream", methods=["GET"])
def stream():
    monitor = current_app.extensions["monitor"]
    retry = current_app.config.get("SSE_RETRY_MILLISECONDS", 5000)

    def event_stream():
        yield f"retry: {retry}\n\n"
        while True:
            event = monitor.event_queue.get()
            data = json.dumps(event)
            yield f"data: {data}\n\n"

    return Response(event_stream(), mimetype="text/event-stream")
