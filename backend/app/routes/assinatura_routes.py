from flask import Blueprint
from app.controllers.plano_controller import PlanoController
from app.middlewares.auth_middleware import jwt_required

class AssinaturaRouter:
    """
    Rotas de Assinaturas (N:N) - Onde o usuário final escolhe/assina um plano.
    """
    def __init__(self):
        self.bp = Blueprint('assinaturas', __name__, url_prefix='/api/assinaturas')
        self.controller = PlanoController()
        self.registrar_rotas()

    def registrar_rotas(self):
        self.bp.add_url_rule('', view_func=jwt_required(self.controller.assinar), methods=['POST'], strict_slashes=False)
        self.bp.add_url_rule('/minhas', view_func=jwt_required(self.controller.minhas_assinaturas), methods=['GET'])
