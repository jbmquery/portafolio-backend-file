# backend_file/src/routes/portafolio_routes.py
from flask import Blueprint
from src.controllers.portafolio_controller import (
    crear_proyecto, obtener_proyectos, obtener_proyecto, actualizar_proyecto, eliminar_proyecto
)

portafolio_bp = Blueprint('portafolio', __name__)

portafolio_bp.route('/api/proyectos', methods=['GET'])(obtener_proyectos)
portafolio_bp.route('/api/proyectos/<int:id>', methods=['GET'])(obtener_proyecto)
portafolio_bp.route('/api/proyectos', methods=['POST'])(crear_proyecto)
portafolio_bp.route('/api/proyectos/<int:id>', methods=['PUT'])(actualizar_proyecto)
portafolio_bp.route('/api/proyectos/<int:id>', methods=['DELETE'])(eliminar_proyecto)