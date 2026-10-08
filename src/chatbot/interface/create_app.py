from pathlib import Path

from flask import Flask, send_from_directory

from src.chatbot.interface.json_error import register_error_handlers
from src.chatbot.interface.routes import chat_route
from src.chatbot.interface.routes import health_route
from src.chatbot.interface.routes import reset_route
from src.chatbot.interface.routes import setup_route
from src.chatbot.interface.routes import setup_status_route

ROOT_DIR = Path(__file__).resolve().parents[3]
DIST_DIR = ROOT_DIR / "frontend" / "dist"
STATIC_DIR = ROOT_DIR / "static"


def create_app(deps) -> Flask:
    has_dist = (DIST_DIR / "index.html").is_file()
    serve_dir = DIST_DIR if has_dist else STATIC_DIR
    app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="/static")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024
    register_error_handlers(app)
    health_route.register(app)
    setup_status_route.register(app, deps)
    setup_route.register(app, deps)
    chat_route.register(app, deps)
    reset_route.register(app, deps)

    @app.route("/")
    def index():
        return send_from_directory(serve_dir, "index.html")

    if has_dist:
        @app.route("/assets/<path:filename>")
        def assets(filename):
            return send_from_directory(DIST_DIR / "assets", filename)

    return app
