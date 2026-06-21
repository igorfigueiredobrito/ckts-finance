from flask import request, jsonify, g
from app.utils.interfaces import InterfaceController
from app.services.plano_service import PlanoService

class PlanoController(InterfaceController):
    def __init__(self):
        self.service = PlanoService()

    def processar_requisicao(self, *args, **kwargs):
        pass

    def listar(self):
        try:
            resultados = self.service.listar_planos()
            return jsonify(resultados), 200
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500

    def criar(self):
        try:
            dados = request.get_json()
            admin_id = getattr(g, 'usuario_id', 0)
            resultado = self.service.criar_plano(admin_id, dados)
            return jsonify(resultado), 201
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 400

    def atualizar(self, plano_id):
        try:
            dados = request.get_json()
            admin_id = getattr(g, 'usuario_id', 0)
            resultado = self.service.atualizar_plano(admin_id, plano_id, dados)
            return jsonify(resultado), 200
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 400

    def deletar(self, plano_id):
        try:
            admin_id = getattr(g, 'usuario_id', 0)
            resultado = self.service.deletar_plano(admin_id, plano_id)
            return jsonify(resultado), 200
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 400

    # --- Controle de Assinaturas (N:N) ---
    def assinar(self):
        try:
            dados = request.get_json()
            plano_id = dados.get('plano_id')
            usuario_id = getattr(g, 'usuario_id', 0)
            
            if not plano_id:
                return jsonify({"erro": True, "mensagem": "O ID do plano é obrigatório."}), 400
                
            resultado = self.service.assinar_plano(usuario_id, plano_id)
            return jsonify(resultado), 200
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 400
        except Exception as e:
            print("ERRO EM ASSINAR:", str(e))
            import traceback
            traceback.print_exc()
            return jsonify({"erro": True, "mensagem": "Erro interno: " + str(e)}), 500

    def minhas_assinaturas(self):
        try:
            usuario_id = getattr(g, 'usuario_id', 0)
            resultado = self.service.minhas_assinaturas(usuario_id)
            return jsonify(resultado), 200
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500
