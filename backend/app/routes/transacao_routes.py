from flask import Blueprint
from app.controllers.transacao_controller import TransacaoController
from app.middlewares.auth_middleware import jwt_required
from app.middlewares.validation_middleware import validate_schema

class TransacaoRouter:
    """
    Classe de Router para Transações.
    """
    def __init__(self):
        self.bp = Blueprint('transacoes', __name__, url_prefix='/api/transacoes')
        self.controller = TransacaoController()
        self._register_routes()

    def _register_routes(self):
        schema_transacao = {
            "descricao": str,
            "valor": (int, float),
            "data": str,
            "categoria_id": int
        }
        
        self.bp.add_url_rule(
            '', 
            view_func=jwt_required(validate_schema(schema_transacao)(self.controller.criar)), 
            methods=['POST']
        )
        
        self.bp.add_url_rule(
            '', 
            view_func=jwt_required(self.controller.listar), 
            methods=['GET']
        )
        
        self.bp.add_url_rule(
            '/<int:id>', 
            view_func=jwt_required(self.controller.ler), 
            methods=['GET']
        )
        
        self.bp.add_url_rule(
            '/<int:id>', 
            view_func=jwt_required(validate_schema(schema_transacao)(self.controller.atualizar)), 
            methods=['PUT']
        )
        
        self.bp.add_url_rule(
            '/all', 
            view_func=jwt_required(self.controller.deletar_todas), 
            methods=['DELETE']
        )
        
        self.bp.add_url_rule(
            '/<int:id>', 
            view_func=jwt_required(self.controller.deletar), 
            methods=['DELETE']
        )

transacao_router = TransacaoRouter()
bp_transacoes = transacao_router.bp
