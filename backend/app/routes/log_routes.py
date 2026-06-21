from flask import Blueprint
from app.controllers.log_controller import LogController
from app.middlewares.auth_middleware import admin_required

class LogRouter:
    """
    Classe de Router para manipulação de Logs.
    """
    def __init__(self):
        self.bp = Blueprint('logs', __name__, url_prefix='/api/logs')
        self.controller = LogController()
        self._register_routes()

    def _register_routes(self):
        self.bp.add_url_rule(
            '/exportar', 
            view_func=admin_required(self.controller.exportar_xml), 
            methods=['GET']
        )

log_router = LogRouter()
bp_logs = log_router.bp
