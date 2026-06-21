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

from flask import request, has_request_context

def _inserir_log(collection_name: str, acao: str, detalhes: dict, usuario: str = None, tabela: str = None, registro_id: int = None):
    ip = None
    user_agent = None
    
    if has_request_context():
        ip = request.remote_addr
        user_agent = request.user_agent.string
        
    documento = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "usuario": usuario,
        "acao": acao,
        "tabela": tabela,
        "registro_id": registro_id,
        "detalhes": detalhes,
        "ip": ip,
        "user_agent": user_agent
    }
    
    try:
        db = mongo_instance.get_db()
        db[collection_name].insert_one(documento)
    except Exception as e:
        print(f"Erro Crítico: Falha ao salvar log '{acao}' na coleção '{collection_name}': {e}")

def registrar_login(usuario: str, ip: str, sucesso: bool):
    detalhes = {
        "sucesso_fracasso": "sucesso" if sucesso else "fracasso"
    }
    _inserir_log("login_logs", "LOGIN", detalhes, usuario=usuario)

def registrar_inclusao(tabela: str, registro_id: int, dados_inseridos: dict, usuario: str):
    detalhes = {
        "dados_inseridos": dados_inseridos
    }
    _inserir_log("auditoria_logs", "INSERT", detalhes, usuario=usuario, tabela=tabela, registro_id=registro_id)

def registrar_alteracao(tabela: str, registro_id: int, antes: dict, depois: dict, usuario: str):
    detalhes = {
        "antes": antes,
        "depois": depois
    }
    _inserir_log("auditoria_logs", "UPDATE", detalhes, usuario=usuario, tabela=tabela, registro_id=registro_id)

def registrar_exclusao(tabela: str, registro_id: int, dados_excluidos: dict, usuario: str):
    detalhes = {
        "dados_excluidos": dados_excluidos
    }
    _inserir_log("auditoria_logs", "DELETE", detalhes, usuario=usuario, tabela=tabela, registro_id=registro_id)
