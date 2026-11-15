from flask import Blueprint, render_template, session, jsonify


bp = Blueprint("main", __name__)


@bp.get("/")
def index():
    return render_template("index.html")

@bp.get("/loggedin")
def logged_in():
    if not session.get("user_id"):
        return jsonify({"logged_in": False})
    return jsonify({"logged_in": True})


# Expose top-level app instance for platforms auto-detecting app/main.py as WSGI entrypoint
class _AppProxy:
    def __init__(self):
        self._app = None

    def _get(self):
        if self._app is None:
            from app import create_app
            self._app = create_app()
        return self._app

    def __call__(self, environ, start_response):
        return self._get()(environ, start_response)

    def __getattr__(self, name):
        return getattr(self._get(), name)


app = _AppProxy()
application = app