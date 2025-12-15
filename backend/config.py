from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "weather.db"

class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FPING_TARGETS = ["8.8.8.8", "1.1.1.1"]
    FPING_INTERVAL_SECONDS = 10
    SSE_RETRY_MILLISECONDS = 5000
    MAX_MEASUREMENTS = 200
