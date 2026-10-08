from flask import jsonify


def register(app) -> None:
    @app.get("/api/health")
    def health():
        return jsonify({"ok": True})
