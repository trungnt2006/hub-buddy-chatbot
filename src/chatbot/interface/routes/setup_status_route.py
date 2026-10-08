from flask import jsonify

from src.chatbot.application.get_setup_status import get_setup_status


def register(app, deps) -> None:
    store = deps["store"]

    @app.get("/api/setup/status")
    def setup_status():
        return jsonify(get_setup_status(store))
