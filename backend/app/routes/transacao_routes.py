from flask import Blueprint
from app.controllers.transacao_controller import TransacaoController
from app.middlewares.auth_middleware import jwt_required
from app.middlewares.validator_middleware import validate_schema

bp_transacoes = Blueprint('transacoes', __name__, url_prefix='/api/transacoes')
controller = TransacaoController()

@bp_transacoes.route('', methods=['POST'])
@jwt_required
@validate_schema({
    "descricao": str,
    "valor": (int, float), # Aceita inteiros ou decimais
    "data": str,
    "categoria_id": int
})
def criar():
    """Cria uma transação autenticada e validada."""
    return controller.criar()

@bp_transacoes.route('', methods=['GET'])
@jwt_required
def listar():
    """Lista as transações do usuário logado."""
    return controller.listar()

@bp_transacoes.route('/<int:id>', methods=['GET'])
@jwt_required
def ler(id):
    """Lê os detalhes de uma transação via ID da URL."""
    return controller.ler(id)

@bp_transacoes.route('/<int:id>', methods=['PUT'])
@jwt_required
@validate_schema({
    "descricao": str,
    "valor": (int, float),
    "data": str,
    "categoria_id": int
})
def atualizar(id):
    """Atualiza a transação baseada no ID e nos dados validados."""
    return controller.atualizar(id)

@bp_transacoes.route('/<int:id>', methods=['DELETE'])
@jwt_required
def deletar(id):
    """Deleta a transação de acordo com o parâmetro de rota."""
    return controller.deletar(id)
