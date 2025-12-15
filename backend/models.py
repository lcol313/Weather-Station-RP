from datetime import datetime
from .database import db


class Measurement(db.Model):
    __tablename__ = "measurements"

    id = db.Column(db.Integer, primary_key=True)
    target = db.Column(db.String(255), nullable=False)
    latency_ms = db.Column(db.Float, nullable=True)
    alive = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "target": self.target,
            "latency_ms": self.latency_ms,
            "alive": self.alive,
            "created_at": self.created_at.isoformat() + "Z",
        }
