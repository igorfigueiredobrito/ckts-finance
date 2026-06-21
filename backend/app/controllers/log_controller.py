from flask import request, jsonify, Response
from app.utils.interfaces import InterfaceController
from app.services.log_service import LogService

class LogController(InterfaceController):
    def __init__(self):
        self.service = LogService()

    def processar_requisicao(self, *args, **kwargs):
        pass

    def exportar_xml(self):
        try:
            usuario = request.args.get('usuario')
            data_inicio = request.args.get('data_inicio')
            data_fim = request.args.get('data_fim')
            
            xml_bytes = self.service.exportar_xml_logs(usuario, data_inicio, data_fim)
            
            return Response(
                xml_bytes,
                mimetype="application/xml",
                headers={"Content-Disposition": "attachment; filename=logs.xml"}
            )
        except Exception as e:
            return jsonify({"erro": True, "mensagem": str(e)}), 500
