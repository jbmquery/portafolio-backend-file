# backend_file/src/controllers/login_controller.py
from flask import request, jsonify
from src.models import AdminUser
from flask_jwt_extended import create_access_token

def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email y contraseña requeridos"}), 400

    user = AdminUser.query.filter_by(email=email).first()
    if user and user.check_password(password):
        token = create_access_token(identity=str(user.id))
        return jsonify(access_token=token), 200
    return jsonify({"msg": "Credenciales inválidas"}), 401