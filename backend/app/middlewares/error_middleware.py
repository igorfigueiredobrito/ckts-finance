import traceback
from flask import request, jsonify, g
from datetime import datetime, timezone
from werkzeug.exceptions import HTTPException
from app.utils.mongo_db import mongo_instance

def register_error_handlers(app):
    """
    Middleware global que captura absolutamente qualquer exceção não tratada
    da aplicação, formatando uma resposta agradável pro Front-End
    e salvando o Stack Trace complexo no MongoDB para debugar mais tarde.
    """
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Extrair status code (Se for HTTP Exception pega o code nativo, senão 500 Interno)
        if isinstance(e, HTTPException):
            status_code = e.code
            mensagem = getattr(e, 'description', str(e))
        else:
            status_code = 500
            mensagem = "Ocorreu um erro interno e inesperado no servidor."

        # Pega a rastreabilidade complexa do erro do Python
        stack_trace = traceback.format_exc()

        try:
            from app.utils.mongo_db import _inserir_log
            # Tenta identificar o usuário se o erro ocorreu numa rota autenticada
            usuario_id = getattr(g, 'usuario_id', None)
            
            detalhes = {
                "erro": str(e),
                "stack_trace": stack_trace,
                "endpoint": request.path,
                "metodo": request.method
            }
            
            # Delega para a nova estrutura de log padronizada
            _inserir_log("error_logs", "ERROR", detalhes, usuario=str(usuario_id) if usuario_id else None)
            
        except Exception as mongo_err:
            print(f"Falha gravíssima: O log de erro não pôde ser gravado. Motivo: {mongo_err}")

        # Retorna o JSON padronizado para o cliente (Frontend/Mobile não quebra)
        return jsonify({
            "erro": True,
            "mensagem": mensagem,
            "codigo": status_code
        }), status_code
