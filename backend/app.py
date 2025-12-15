from flask import Flask

from .config import Config
from .database import init_db
from .monitor import Monitor
from .routes import bp as api_bp


def create_app(config: type[Config] = Config):
    app = Flask(__name__)
    app.config.from_object(config)

    init_db(app)

    monitor = Monitor(
        targets=app.config["FPING_TARGETS"],
        interval_seconds=app.config["FPING_INTERVAL_SECONDS"],
    )
    monitor.start()
    app.extensions["monitor"] = monitor

    app.register_blueprint(api_bp, url_prefix="/api")

    return app


def run():
    flask_app = create_app()
    flask_app.run(host="0.0.0.0", port=8000, debug=True)


if __name__ == "__main__":
    run()
