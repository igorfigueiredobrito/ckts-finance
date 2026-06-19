from flask import jsonify, g, request
from app.utils.interfaces import InterfaceController
from app.services.categoria_service import CategoriaService

class CategoriaController(InterfaceController):
    """
    Controller para orquestrar requisições HTTP relacionadas a Categorias.
    """
    def __init__(self):
        self.service = CategoriaService()

    def processar_requisicao(self, *args, **kwargs):
        pass

    def listar(self):
        try:
            usuario_id = g.usuario_id
            resultado = self.service.listar_categorias_usuario(usuario_id)
            return jsonify(resultado), 200
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500

    def criar(self):
        try:
            dados = request.get_json()
            resultado = self.service.criar_categoria(g.usuario_id, dados)
            return jsonify(resultado), 201
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 400
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500

    def atualizar(self, id):
        try:
            dados = request.get_json()
            resultado = self.service.atualizar_categoria(id, g.usuario_id, dados)
            return jsonify(resultado), 200
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 400
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500

    def deletar(self, id):
        try:
            resultado = self.service.deletar_categoria(id, g.usuario_id)
            return jsonify(resultado), 200
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 400
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500
