from functools import wraps
from flask import request, jsonify, g
import jwt
import os

def jwt_required(f):
    """
    Middleware/Decorator para proteger rotas.
    Exige um JWT válido no Header 'Authorization: Bearer <token>'
    Se válido, injeta os dados do usuário em 'g' para as próximas camadas.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                "erro": "Acesso Negado", 
                "mensagem": "Token JWT não fornecido ou no formato incorreto."
            }), 401
            
        # Extrai a string do token
        token = auth_header.split(" ")[1]
        
        try:
            secret = os.getenv('JWT_SECRET', 'super_secret')
            # Valida e decodifica o token
            decoded = jwt.decode(token, secret, algorithms=["HS256"])
            
            # Injeta variáveis no contexto de requisição (disponível para Controllers/Services)
            g.usuario_id = decoded.get("usuario_id")
            g.usuario_email = decoded.get("email")
            
        except jwt.ExpiredSignatureError:
            return jsonify({
                "erro": "Token Expirado", 
                "mensagem": "Seu token expirou, faça login novamente."
            }), 401
        except jwt.InvalidTokenError:
            return jsonify({
                "erro": "Token Inválido", 
                "mensagem": "O token fornecido é inválido ou foi adulterado."
            }), 401
            
        return f(*args, **kwargs)
        
    return decorated_function
