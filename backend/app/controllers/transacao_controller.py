from flask import request, jsonify, g
from app.utils.interfaces import InterfaceController
from app.services.transacao_service import TransacaoService

class TransacaoController(InterfaceController):
    """
    Camada de Controle para Transações Financeiras.
    """
    def __init__(self):
        self.service = TransacaoService()

    def processar_requisicao(self, *args, **kwargs):
        pass

    def criar(self):
        try:
            dados = request.get_json()
            usuario_id = g.usuario_id # Recuperado via Middleware de Auth
            resultado = self.service.criar_transacao(dados, usuario_id)
            return jsonify(resultado), 201
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 400

    def listar(self):
        try:
            usuario_id = g.usuario_id
            filtros = {
                "descricao": request.args.get('descricao'),
                "start_date": request.args.get('start_date'),
                "end_date": request.args.get('end_date')
            }
            resultado = self.service.listar_transacoes(usuario_id, **filtros)
            return jsonify(resultado), 200
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500

    def ler(self, transacao_id):
        try:
            usuario_id = g.usuario_id
            resultado = self.service.ler_transacao(transacao_id, usuario_id)
            return jsonify(resultado), 200
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 404

    def atualizar(self, transacao_id):
        try:
            dados = request.get_json()
            usuario_id = g.usuario_id
            resultado = self.service.atualizar_transacao(transacao_id, dados, usuario_id)
            return jsonify(resultado), 200
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 400

    def deletar(self, transacao_id):
        try:
            usuario_id = g.usuario_id
            resultado = self.service.deletar_transacao(transacao_id, usuario_id)
            return jsonify(resultado), 200
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 403
