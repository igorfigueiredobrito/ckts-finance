from flask import Blueprint
from app.controllers.usuario_controller import UsuarioController
from app.middlewares.validator_middleware import validate_schema
from app.middlewares.auth_middleware import jwt_required

bp_usuarios = Blueprint('usuarios', __name__, url_prefix='/api/usuarios')
controller = UsuarioController()

@bp_usuarios.route('/registrar', methods=['POST'])
@validate_schema({
    "nome": str,
    "email": str,
    "senha": str,
    "foto_perfil": str
})
def registrar():
    """
    Rota Pública para Registro de Usuários.
    Usa o middleware de validação para garantir a integridade do JSON.
    """
    return controller.registrar()

@bp_usuarios.route('/login', methods=['POST'])
@validate_schema({
    "email": str,
    "senha": str
})
def login():
    """
    Rota Pública para Login (Geração do Token JWT).
    """
    return controller.login()

@bp_usuarios.route('/upload-foto', methods=['POST'])
def upload_foto():
    """
    Recebe imagem via Form-Data e salva fisicamente no backend, 
    retornando a URL gerada para ser enviada no Cadastro.
    """
    return controller.upload_foto()

@bp_usuarios.route('/perfil', methods=['PUT'])
@jwt_required
def atualizar_perfil():
    """
    Atualiza os dados do usuário logado (nome, email, senha e foto).
    """
    return controller.atualizar_perfil()
