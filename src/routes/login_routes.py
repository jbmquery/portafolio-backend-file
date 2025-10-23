# backend_file/src/routes/login_routes.py
from flask import Blueprint
from src.controllers.login_controller import login

login_bp = Blueprint('login', __name__)

@login_bp.route('/api/login', methods=['POST'])
def login_route():
    return login()