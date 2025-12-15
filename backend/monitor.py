import json
import queue
import subprocess
import threading
import time
from datetime import datetime
from typing import Iterable, List

from .database import db
from .models import Measurement


class Monitor:
    def __init__(self, targets: Iterable[str], interval_seconds: int = 10):
        self.targets: List[str] = list(targets)
        self.interval_seconds = interval_seconds
        self._queue: "queue.Queue[dict]" = queue.Queue()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    @property
    def event_queue(self) -> "queue.Queue[dict]":
        return self._queue

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=2)

    def _run_loop(self):
        while not self._stop_event.is_set():
            for target in self.targets:
                measurement = self._ping_target(target)
                db.session.add(measurement)
                db.session.commit()
                payload = measurement.to_dict()
                self._queue.put(payload)
            time.sleep(self.interval_seconds)

    def _ping_target(self, target: str) -> Measurement:
        command = ["fping", "-e", "-c", "1", target]
        completed = subprocess.run(command, capture_output=True, text=True)
        output = completed.stdout.strip() or completed.stderr.strip()
        alive = completed.returncode == 0
        latency_ms = None

        if alive:
            latency_ms = self._extract_latency(output)

        return Measurement(target=target, latency_ms=latency_ms, alive=alive, created_at=datetime.utcnow())

    @staticmethod
    def _extract_latency(output: str) -> float | None:
        # Expected success output example: "8.8.8.8 : [0], 84 bytes, 12.8 ms (12.8 avg, 0% loss)"
        for token in output.split():
            if token.endswith("ms"):
                value = token.replace("ms", "")
                try:
                    return float(value)
                except ValueError:
                    continue
        return None

    def recent_events(self, limit: int) -> list[dict]:
        measurements = (
            Measurement.query.order_by(Measurement.created_at.desc()).limit(limit).all()
        )
        return [item.to_dict() for item in measurements]

    def export_history(self, limit: int = 500) -> str:
        measurements = (
            Measurement.query.order_by(Measurement.created_at.desc()).limit(limit).all()
        )
        return json.dumps([m.to_dict() for m in measurements], indent=2)
