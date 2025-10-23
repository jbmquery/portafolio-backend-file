# backend_file/main.py
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from src.models import db
from src.routes.login_routes import login_bp
from src.routes.portafolio_routes import portafolio_bp
import os


app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5173",
    "https://jbm-portafolio.netlify.app",
    "https://jbm-portafolio.com"
])

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "fallback-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
JWTManager(app)

app.register_blueprint(login_bp)
app.register_blueprint(portafolio_bp)


with app.app_context():
    db.create_all()
    from src.models import AdminUser
    if not AdminUser.query.first():
        admin = AdminUser(email="admin@portafolio.com")
        admin.set_password("securepassword123")
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario admin creado")

if __name__ == '__main__':
    app.run(debug=True)