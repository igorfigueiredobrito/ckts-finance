from flask import request, jsonify
from app.utils.interfaces import InterfaceController
from app.services.admin_service import AdminService

class AdminController(InterfaceController):
    def __init__(self):
        self.service = AdminService()

    def processar_requisicao(self, *args, **kwargs):
        pass

    def listar_usuarios(self):
        try:
            usuarios = self.service.listar_usuarios()
            return jsonify(usuarios), 200
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500

    def alternar_status_usuario(self, id):
        try:
            resultado = self.service.alternar_status_usuario(id)
            return jsonify(resultado), 200
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 400
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500

    def estatisticas(self):
        try:
            stats = self.service.estatisticas_gerais()
            return jsonify(stats), 200
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500

    def deletar_usuario(self, id):
        try:
            resultado = self.service.deletar_usuario(id)
            return jsonify(resultado), 200
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 400
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500

