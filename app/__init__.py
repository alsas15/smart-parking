from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()

def create_app() -> Flask:
    from .routes import bp

    app = Flask(__name__)
    app.config.from_object("app.config.Config")
    db.init_app(app)

    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()

    return app
