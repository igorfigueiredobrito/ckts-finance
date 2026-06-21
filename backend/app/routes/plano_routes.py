from flask import Blueprint
from app.controllers.plano_controller import PlanoController
from app.middlewares.auth_middleware import admin_required, jwt_required

class PlanoRouter:
    """
    Rotas gerenciais de Planos (Apenas Admin pode criar, editar ou excluir planos).
    """
    def __init__(self):
        self.bp = Blueprint('planos', __name__, url_prefix='/api/planos')
        self.controller = PlanoController()
        self.registrar_rotas()

    def registrar_rotas(self):
        # Leitura é pública para quem está logado poder ver os cards
        self.bp.add_url_rule('', view_func=jwt_required(self.controller.listar), methods=['GET'], strict_slashes=False)
        
        # Criação, Edição e Exclusão são restritas ao Admin
        self.bp.add_url_rule('', view_func=admin_required(self.controller.criar), methods=['POST'], strict_slashes=False)
        self.bp.add_url_rule('/<int:plano_id>', view_func=admin_required(self.controller.atualizar), methods=['PUT'])
        self.bp.add_url_rule('/<int:plano_id>', view_func=admin_required(self.controller.deletar), methods=['DELETE'])
