import time
from flask import request, g
from datetime import datetime, timezone
from app.utils.mongo_db import mongo_instance

def register_log_middleware(app):
    """
    Intercepta as requisições para computar o tempo de resposta e
    registrar de forma analítica no MongoDB (Logs de Acesso/Analytics).
    """
    
    @app.before_request
    def start_timer():
        # Guarda o timestamp do inicio da requisição no contexto 'g'
        g.start_time = time.time()

    @app.after_request
    def log_request(response):
        # Evita logar pre-flights (OPTIONS) comuns em CORS
        if request.method == 'OPTIONS':
            return response
            
        try:
            # Calcula o tempo total em milissegundos
            process_time = time.time() - g.start_time
            process_time_ms = round(process_time * 1000, 2)
            
            # O auth_middleware deve popular o 'usuario_id' no contexto 'g' se houver login
            usuario_id = getattr(g, 'usuario_id', None)
            
            log_data = {
                "endpoint": request.path,
                "method": request.method,
                "usuario_id": usuario_id,
                "timestamp": datetime.now(timezone.utc),
                "ip": request.remote_addr,
                "status_code": response.status_code,
                "response_time_ms": process_time_ms
            }
            
            # Insere no MongoDB na coleção 'request_logs'
            db = mongo_instance.get_db()
            db.request_logs.insert_one(log_data)
            
        except Exception as e:
            print(f"Erro Crítico: Falha ao registrar log da requisição no MongoDB: {e}")
            
        return response
