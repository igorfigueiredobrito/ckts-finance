from pymongo import MongoClient
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

class MongoHelper:
    """
    Implementação do Padrão Singleton para gerenciar a conexão com o MongoDB.
    Garante que o pool de conexões do PyMongo seja reutilizado eficientemente.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoHelper, cls).__new__(cls)
            cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        db_name = os.getenv('MONGO_DB_NAME', 'finance_logs')
        # Inicializa o MongoClient
        self.client = MongoClient(mongo_uri)
        # Seleciona o banco de dados
        self.db = self.client[db_name]
        
    def get_db(self):
        return self.db

# Instância global do MongoDB
mongo_instance = MongoHelper()

def registrar_auditoria(acao: str, tabela: str, registro_id: int, usuario_id: int):
    """
    Registra no MongoDB as ações Críticas do sistema.
    :param acao: 'INCLUSAO', 'ALTERACAO' ou 'EXCLUSAO'
    :param tabela: Nome da tabela no MySQL afetada
    :param registro_id: ID do registro afetado
    :param usuario_id: ID do usuário que realizou a ação
    """
    try:
        db = mongo_instance.get_db()
        documento = {
            "acao": acao.upper(),
            "tabela": tabela,
            "registro_id": registro_id,
            "usuario_id": usuario_id,
            "timestamp": datetime.now(timezone.utc)
        }
        # Salva na coleção (tabela NoSQL) 'auditoria_logs'
        db.auditoria_logs.insert_one(documento)
    except Exception as e:
        # Em um sistema real, falhas de log não devem quebrar a ação principal, 
        # mas devem gerar alertas em ferramentas como Sentry/Datadog.
        print(f"Erro Crítico: Falha ao salvar log de auditoria no MongoDB: {e}")
