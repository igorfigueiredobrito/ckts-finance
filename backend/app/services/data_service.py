import json
import xml.etree.ElementTree as ET
from datetime import datetime
from app.utils.interfaces import InterfaceService
from app.services.transacao_service import TransacaoService
from app.utils.mongo_db import mongo_instance

class DataService(InterfaceService):
    """
    Camada de serviço específica para operações massivas e serialização (Import/Export).
    """
    def __init__(self):
        self.transacao_service = TransacaoService()

    def executar_regras_negocio(self, *args, **kwargs):
        pass

    def exportar_json(self, usuario_id: int) -> str:
        # Reutilizamos o Service de transações para buscar dados já validados
        transacoes_raw = self.transacao_service.listar_transacoes(usuario_id)
        
        # O banco pode retornar objetos `datetime` ou `date`. 
        # Precisamos converter para string ISO antes de serializar no JSON.
        for t in transacoes_raw:
            if isinstance(t.get('data'), datetime) or hasattr(t.get('data'), 'isoformat'):
                t['data'] = t['data'].isoformat()
            if isinstance(t.get('created_at'), datetime) or hasattr(t.get('created_at'), 'isoformat'):
                t['created_at'] = t['created_at'].isoformat()
                
        # Gera o JSON formatado com 4 espaços de identação
        json_string = json.dumps(transacoes_raw, indent=4, default=str, ensure_ascii=False)
        return json_string

    def importar_json(self, arquivo_content: bytes, usuario_id: int) -> dict:
        try:
            # Desserializa os bytes vindos do upload para um objeto Python
            dados = json.loads(arquivo_content.decode('utf-8'))
        except json.JSONDecodeError as e:
            raise ValueError(f"O arquivo enviado não é um JSON válido: {str(e)}")

        if not isinstance(dados, list):
            raise ValueError("A estrutura do arquivo JSON deve ser uma lista de transações: [...]")

        importados_com_sucesso = 0
        erros_no_lote = []

        # Fazemos a persistência parcial: se uma transação falhar, pulamos e continuamos.
        for idx, transacao in enumerate(dados):
            try:
                # Validação super básica para não estourar na DAO
                if not all(k in transacao for k in ('descricao', 'valor', 'data', 'categoria_id')):
                    raise ValueError("Transação não possui todos os campos obrigatórios.")

                # A própria TransacaoService já aplica as regras de negócio (ex: valor não negativo)
                self.transacao_service.criar_transacao(transacao, usuario_id)
                importados_com_sucesso += 1
            except Exception as e:
                # Armazena o erro para devolver no feedback final
                erros_no_lote.append({"indice": idx, "motivo": str(e)})

        # O log de auditoria agora é feito individualmente dentro de transacao_service.criar_transacao
        
        return {
            "sucesso": True,
            "importados": importados_com_sucesso,
            "falhas": len(erros_no_lote),
            "detalhes_falhas": erros_no_lote
        }

    def exportar_xml_logs(self, start_date: str = None, end_date: str = None) -> bytes:
        db = mongo_instance.get_db()
        query = {}
        
        # Cria a query de filtro por intervalo de datas se os parâmetros existirem
        if start_date or end_date:
            timestamp_query = {}
            if start_date:
                try:
                    timestamp_query["$gte"] = datetime.fromisoformat(start_date)
                except Exception:
                    pass
            if end_date:
                try:
                    timestamp_query["$lte"] = datetime.fromisoformat(end_date)
                except Exception:
                    pass
            if timestamp_query:
                query["timestamp"] = timestamp_query

        # Busca no Mongo (focando na coleção de auditoria)
        # Atenção: As novas chaves são "data_hora", "usuario", e não há "acao".
        logs = db.auditoria_logs.find(query)
        
        # Usa a lib nativa ElementTree para construir os Nodos do XML
        root = ET.Element("logs")
        
        for doc in logs:
            evento = ET.SubElement(root, "evento", id=str(doc.get('_id', '')))
            
            # A ação agora vem do próprio doc.get("acao")
            acao = str(doc.get("acao", "DESCONHECIDO"))
            
            ET.SubElement(evento, "acao").text = acao
            ET.SubElement(evento, "tabela").text = str(doc.get("tabela", ""))
            ET.SubElement(evento, "registro_id").text = str(doc.get("registro_id", ""))
            ET.SubElement(evento, "usuario").text = str(doc.get("usuario", ""))
            
            # Formatação do timestamp
            ts = doc.get("timestamp")
            if ts:
                ts_str = ts.isoformat() if hasattr(ts, 'isoformat') else str(ts)
                ET.SubElement(evento, "timestamp").text = ts_str

            # Detalhes (pode conter dados da assinatura, ou valores antigos/novos)
            detalhes = doc.get("detalhes")
            if detalhes:
                try:
                    ET.SubElement(evento, "detalhes").text = json.dumps(detalhes, ensure_ascii=False)
                except Exception:
                    ET.SubElement(evento, "detalhes").text = str(detalhes)
                
        # Serializa para binário, adicionando a declaração <?xml ...?>
        xml_bytes = ET.tostring(root, encoding="utf-8", xml_declaration=True)
        return xml_bytes
