from functools import wraps
from flask import request, jsonify

def validate_schema(schema: dict):
    """
    Middleware para realizar a validação prévia dos payloads (JSON body).
    Evita que dados inúteis ou tipagens incorretas cheguem no Controller/Service.
    
    :param schema: Dicionário onde a chave é o nome do campo e o valor é o tipo base nativo.
    Exemplo: validate_schema({"nome": str, "idade": int, "salario": float})
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not request.is_json:
                return jsonify({
                    "erro": "Bad Request", 
                    "mensagem": "O Content-Type deve ser obrigatoriamente 'application/json'"
                }), 400
                
            data = request.get_json()
            erros = []
            
            # Percorre as regras exigidas no schema da rota
            for campo, tipo_esperado in schema.items():
                if campo not in data:
                    erros.append(f"O campo obrigatório '{campo}' está ausente.")
                elif not isinstance(data[campo], tipo_esperado):
                    erros.append(f"O campo '{campo}' deveria ser do tipo '{tipo_esperado.__name__}'.")
                    
            if erros:
                return jsonify({
                    "erro": "Falha na Validação", 
                    "detalhes": erros
                }), 400
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator
