from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # Importar y registrar los blueprints
    from app.routes import main  # Rutas principales
    from app.auth_routes import auth  # Rutas de autenticación
    from app.ticket_routes import tickets  # Rutas para gestión de tickets

    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(tickets, url_prefix='/tickets')  # Prefijo para las rutas de tickets

    return app