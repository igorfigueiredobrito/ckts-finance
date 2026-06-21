from flask import Blueprint
from app.controllers.usuario_controller import UsuarioController
from app.middlewares.validation_middleware import validate_schema
from app.middlewares.auth_middleware import jwt_required

class UsuarioRouter:
    """
    Classe de Router para Usuários.
    Agrupa as rotas e associa aos métodos do UsuarioController,
    sem conter nenhuma regra de negócio.
    """
    def __init__(self):
        self.bp = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')
        self.controller = UsuarioController()
        self._register_routes()

    def _register_routes(self):
        # /registrar
        schema_registro = {
            "nome": str,
            "email": str,
            "senha": str,
            "telefone": str,
            "cpf": str,
            "data_nascimento": str,
            "foto_perfil": (str, type(None))
        }
        self.bp.add_url_rule(
            '/registrar', 
            view_func=validate_schema(schema_registro)(self.controller.registrar), 
            methods=['POST']
        )
        
        # /login
        schema_login = {
            "email": str,
            "senha": str
        }
        self.bp.add_url_rule(
            '/login', 
            view_func=validate_schema(schema_login)(self.controller.login), 
            methods=['POST']
        )
        
        # /upload-foto
        self.bp.add_url_rule(
            '/upload-foto', 
            view_func=self.controller.upload_foto, 
            methods=['POST']
        )
        
        # /perfil
        self.bp.add_url_rule(
            '/perfil', 
            view_func=jwt_required(self.controller.atualizar_perfil), 
            methods=['PUT']
        )

# Instância que será importada pelo __init__.py
usuario_router = UsuarioRouter()
bp_usuarios = usuario_router.bp
