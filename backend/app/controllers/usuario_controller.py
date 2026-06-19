from flask import request, jsonify, g
from app.utils.interfaces import InterfaceController
from app.services.usuario_service import UsuarioService

class UsuarioController(InterfaceController):
    """
    Camada de Controle responsável por receber as requests do Flask
    e delegar para o Serviço de Usuários.
    """
    def __init__(self):
        self.service = UsuarioService()

    def processar_requisicao(self, *args, **kwargs):
        pass

    def registrar(self):
        try:
            dados = request.get_json()
            resultado = self.service.criar_usuario(dados)
            return jsonify(resultado), 201
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 400
            
    def login(self):
        try:
            dados = request.get_json()
            email = dados.get("email")
            senha = dados.get("senha")
            resultado = self.service.realizar_login(email, senha)
            return jsonify(resultado), 200
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 401

    def atualizar_perfil(self):
        try:
            dados = request.get_json()
            usuario_id = g.usuario_id
            resultado = self.service.atualizar_usuario(usuario_id, dados)
            return jsonify(resultado), 200
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 400

    def upload_foto(self):
        try:
            import os
            import uuid
            from werkzeug.utils import secure_filename
            
            if 'file' not in request.files:
                return jsonify({"erro": True, "mensagem": "Nenhum arquivo enviado com a key 'file'"}), 400
                
            arquivo = request.files['file']
            if arquivo.filename == '':
                return jsonify({"erro": True, "mensagem": "Arquivo inválido"}), 400
                
            filename = secure_filename(arquivo.filename)
            ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'jpg'
            novo_nome = f"{uuid.uuid4().hex}.{ext}"
            
            # Caminho absoluto da pasta app/static/uploads
            pasta_destino = os.path.join(os.path.dirname(__file__), '..', 'static', 'uploads')
            os.makedirs(pasta_destino, exist_ok=True)
            
            filepath = os.path.join(pasta_destino, novo_nome)
            arquivo.save(filepath)
            
            # Retorna o path relativo que será salvo no banco
            url = f"/static/uploads/{novo_nome}"
            return jsonify({"url": url, "mensagem": "Upload concluído"}), 200
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500
