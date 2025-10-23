# backend_file/main.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.models import db, AdminUser
import os


def create_app():
    app = Flask(__name__)

    # Configurar CORS con los orígenes permitidos (frontend en desarrollo y producción)
    CORS(app, origins=[
        "http://localhost:5173",
        "https://jbm-portafolio.netlify.app",
        "https://jbm-portafolio.com"
    ])

    # Configuración desde variables de entorno
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "fallback-secret-for-dev-only")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar extensiones
    db.init_app(app)
    JWTManager(app)

    # Registrar blueprints
    from src.routes.login_routes import login_bp
    from src.routes.portafolio_routes import portafolio_bp
    app.register_blueprint(login_bp)
    app.register_blueprint(portafolio_bp)

    # Crear tablas y usuario admin si no existen
    with app.app_context():
        db.create_all()
        if not AdminUser.query.first():
            admin_email = os.environ.get("ADMIN_EMAIL", "admin@portafolio.com")
            admin_password = os.environ.get("ADMIN_PASSWORD", "securepassword123")
            admin = AdminUser(email=admin_email)
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print("✅ Tablas y usuario admin creados")

    return app


# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    # Solo para desarrollo local
    app.run(debug=True)