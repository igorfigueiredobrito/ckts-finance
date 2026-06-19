from flask import Blueprint
from app.controllers.categoria_controller import CategoriaController
from app.middlewares.auth_middleware import jwt_required
from app.middlewares.validator_middleware import validate_schema

bp_categorias = Blueprint('categorias', __name__, url_prefix='/api/categorias')
controller = CategoriaController()

@bp_categorias.route('', methods=['GET'])
@jwt_required
def listar():
    """
    Rota para listar todas as categorias do usuário logado.
    """
    return controller.listar()

@bp_categorias.route('', methods=['POST'])
@jwt_required
@validate_schema({ "nome": str, "tipo": str })
def criar():
    return controller.criar()

@bp_categorias.route('/<int:id>', methods=['PUT'])
@jwt_required
@validate_schema({ "nome": str, "tipo": str })
def atualizar(id):
    return controller.atualizar(id)

@bp_categorias.route('/<int:id>', methods=['DELETE'])
@jwt_required
def deletar(id):
    return controller.deletar(id)
