from flask import Blueprint
from app.controllers.categoria_controller import CategoriaController
from app.middlewares.auth_middleware import jwt_required
from app.middlewares.validation_middleware import validate_schema

class CategoriaRouter:
    """
    Classe de Router para Categorias.
    """
    def __init__(self):
        self.bp = Blueprint('categorias', __name__, url_prefix='/api/categorias')
        self.controller = CategoriaController()
        self._register_routes()

    def _register_routes(self):
        schema_categoria = { "nome": str, "tipo": str }
        
        self.bp.add_url_rule(
            '', 
            view_func=jwt_required(self.controller.listar), 
            methods=['GET']
        )
        
        self.bp.add_url_rule(
            '', 
            view_func=jwt_required(validate_schema(schema_categoria)(self.controller.criar)), 
            methods=['POST']
        )
        
        self.bp.add_url_rule(
            '/<int:id>', 
            view_func=jwt_required(validate_schema(schema_categoria)(self.controller.atualizar)), 
            methods=['PUT']
        )
        
        self.bp.add_url_rule(
            '/<int:id>', 
            view_func=jwt_required(self.controller.deletar), 
            methods=['DELETE']
        )

categoria_router = CategoriaRouter()
bp_categorias = categoria_router.bp
