from flask import Blueprint
from app.controllers.admin_controller import AdminController
from app.middlewares.auth_middleware import admin_required

class AdminRouter:
    """
    Classe de Router para Administração.
    """
    def __init__(self):
        self.bp = Blueprint('admin', __name__, url_prefix='/api/admin')
        self.controller = AdminController()
        self._register_routes()

    def _register_routes(self):
        self.bp.add_url_rule(
            '/usuarios', 
            view_func=admin_required(self.controller.listar_usuarios), 
            methods=['GET']
        )
        
        self.bp.add_url_rule(
            '/usuarios/<int:id>/status', 
            view_func=admin_required(self.controller.alternar_status_usuario), 
            methods=['PATCH']
        )
        
        self.bp.add_url_rule(
            '/stats', 
            view_func=admin_required(self.controller.estatisticas), 
            methods=['GET']
        )
        
        self.bp.add_url_rule(
            '/usuarios/<int:id>', 
            view_func=admin_required(self.controller.deletar_usuario), 
            methods=['DELETE']
        )

admin_router = AdminRouter()
bp_admin = admin_router.bp
