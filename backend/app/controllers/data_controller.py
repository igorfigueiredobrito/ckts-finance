from flask import request, jsonify, g, Response
from app.utils.interfaces import InterfaceController
from app.services.data_service import DataService

class DataController(InterfaceController):
    """
    Camada de Controle que lida com upload de arquivos (multipart) 
    e geração de arquivos para download via Flask Response.
    """
    def __init__(self):
        self.service = DataService()

    def processar_requisicao(self, *args, **kwargs):
        pass

    def exportar_json(self):
        try:
            usuario_id = g.usuario_id
            json_string = self.service.exportar_json(usuario_id)
            
            # Formata a resposta forçando o Download Automático no navegador
            return Response(
                json_string,
                mimetype="application/json",
                headers={"Content-Disposition": "attachment;filename=exportacao_transacoes.json"}
            )
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500

    def importar_json(self):
        try:
            usuario_id = g.usuario_id
            
            # Valida se a requisição veio como multipart/form-data e contém a key 'file'
            if 'file' not in request.files:
                return jsonify({"erro": True, "mensagem": "Nenhum arquivo enviado com a chave 'file'"}), 400
                
            arquivo = request.files['file']
            
            # Validação rasa de segurança (Extensão)
            if arquivo.filename == '' or not arquivo.filename.endswith('.json'):
                return jsonify({"erro": True, "mensagem": "Arquivo inválido. Deve ser no formato .json"}), 400
                
            arquivo_bytes = arquivo.read()
            resultado = self.service.importar_json(arquivo_bytes, usuario_id)
            
            return jsonify(resultado), 200
        except ValueError as ve:
            return jsonify({"erro": True, "mensagem": str(ve)}), 400
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500

    def exportar_xml_logs(self):
        try:
            # Pega os parâmetros da URL, caso enviados (ex: ?start_date=2023-01-01)
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            
            xml_bytes = self.service.exportar_xml_logs(start_date, end_date)
            
            return Response(
                xml_bytes,
                mimetype="application/xml",
                headers={"Content-Disposition": "attachment;filename=auditoria_mongo.xml"}
            )
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500
