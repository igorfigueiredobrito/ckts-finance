import xml.etree.ElementTree as ET
from xml.dom import minidom
from app.utils.interfaces import InterfaceService
from app.utils.mongo_db import mongo_instance
from datetime import datetime

class LogService(InterfaceService):
    def executar_regras_negocio(self, *args, **kwargs):
        pass
        
    def exportar_xml_logs(self, usuario: str, data_inicio: str, data_fim: str) -> bytes:
        db = mongo_instance.get_db()
        
        query = {}
        if usuario:
            query["usuario"] = usuario
            
        if data_inicio or data_fim:
            date_filter = {}
            if data_inicio:
                # Add basic start string filter (assuming isoformat matching roughly or proper parsing)
                # Since we stored as ISO format string: "2025-01-15T14:30:00+00:00"
                # Lexicographical compare works if both are ISO.
                date_filter["$gte"] = data_inicio
            if data_fim:
                # To include the entire day if only YYYY-MM-DD is given
                date_filter["$lte"] = data_fim + "T23:59:59"
            query["timestamp"] = date_filter
            
        collections = ["auditoria_logs", "login_logs", "error_logs", "request_logs"]
        all_logs = []
        for col in collections:
            all_logs.extend(list(db[col].find(query)))
            
        def get_time_str(log):
            t = log.get("timestamp") or log.get("data_hora") or ""
            if isinstance(t, datetime):
                return t.isoformat()
            return str(t)
            
        # Ordenar por timestamp
        all_logs.sort(key=get_time_str)
        
        # Build XML
        root = ET.Element("logs")
        
        for idx, log in enumerate(all_logs, start=1):
            evento = ET.SubElement(root, "evento", id=str(idx))
            
            # <usuario>
            usr = log.get("usuario")
            ET.SubElement(evento, "usuario").text = str(usr) if usr else "N/A"
            
            # <acao>
            acao = log.get("acao", "UNKNOWN")
            ET.SubElement(evento, "acao").text = acao
            
            # <descricao> & <tipo_evento>
            tipo_evento, descricao = self._mapear_acao(acao, log)
            ET.SubElement(evento, "descricao").text = descricao
            
            # <data_hora>
            ET.SubElement(evento, "data_hora").text = get_time_str(log)
            
            # <tipo_evento>
            ET.SubElement(evento, "tipo_evento").text = tipo_evento
            
            # <ip_origem>
            ip = log.get("ip")
            ET.SubElement(evento, "ip_origem").text = str(ip) if ip else "N/A"
            
            # <dados_vinculados> (Condicional)
            if acao in ["INSERT", "UPDATE", "DELETE"]:
                tabela = log.get("tabela")
                registro_id = log.get("registro_id")
                if tabela or registro_id:
                    dados_vinc = ET.SubElement(evento, "dados_vinculados")
                    ET.SubElement(dados_vinc, "tabela").text = str(tabela) if tabela else ""
                    ET.SubElement(dados_vinc, "registro_id").text = str(registro_id) if registro_id else ""
                    
        # Converter para string com pretty print (identado)
        xml_str = ET.tostring(root, encoding="utf-8")
        parsed = minidom.parseString(xml_str)
        pretty_xml_str = parsed.toprettyxml(indent="  ", encoding="UTF-8")
        
        return pretty_xml_str

    def _mapear_acao(self, acao: str, log: dict):
        detalhes = log.get("detalhes", {})
        if acao == "LOGIN":
            sucesso = detalhes.get("sucesso_fracasso")
            msg = "Usuário autenticado com sucesso" if sucesso == "sucesso" else "Falha na autenticação"
            return "autenticacao", msg
        elif acao == "INSERT":
            return "cadastro", "Novo registro inserido no sistema"
        elif acao == "UPDATE":
            return "alteracao", "Registro atualizado no sistema"
        elif acao == "DELETE":
            return "exclusao", "Registro deletado do sistema"
        elif acao == "ERROR":
            return "erro_sistema", "Erro interno da aplicação"
        elif acao == "ACCESS":
            return "acesso_rota", f"Acesso à rota {detalhes.get('endpoint', '')}"
        return "outro", "Ação desconhecida"
