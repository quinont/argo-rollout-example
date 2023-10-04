import os

from flask import Flask


def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev"
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/check")
    def check():
        return "OK"

    from frontend import frontend
    app.register_blueprint(frontend.bp)

    app.add_url_rule("/", endpoint="index")

    return app

