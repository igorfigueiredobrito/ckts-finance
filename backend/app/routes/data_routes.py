from flask import Blueprint
from app.controllers.data_controller import DataController
from app.middlewares.auth_middleware import jwt_required

class DataRouter:
    """
    Classe de Router para manipulação de Dados (Import/Export).
    """
    def __init__(self):
        self.bp = Blueprint('data', __name__, url_prefix='/api/data')
        self.controller = DataController()
        self._register_routes()

    def _register_routes(self):
        self.bp.add_url_rule(
            '/export/transacoes/json', 
            view_func=jwt_required(self.controller.exportar_json), 
            methods=['GET']
        )
        
        self.bp.add_url_rule(
            '/import/transacoes/json', 
            view_func=jwt_required(self.controller.importar_json), 
            methods=['POST']
        )
        
        self.bp.add_url_rule(
            '/export/logs/xml', 
            view_func=jwt_required(self.controller.exportar_xml_logs), 
            methods=['GET']
        )

data_router = DataRouter()
bp_data = data_router.bp
