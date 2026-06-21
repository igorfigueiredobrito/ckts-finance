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
            g.usuario_role = decoded.get("role")
            
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

def admin_required(f):
    """
    Middleware que primeiro exige o JWT válido, e depois verifica a role de Admin.
    """
    @wraps(f)
    @jwt_required
    def decorated_function(*args, **kwargs):
        # O jwt_required já decodificou e injetou no 'g', 
        # mas a role a gente precisa puxar novamente ou apenas ler do header
        # Para ser mais robusto, o jwt_required já poderia injetar a role.
        # Vamos atualizar o jwt_required para injetar g.usuario_role
        if not getattr(g, 'usuario_role', None) == 'admin':
            return jsonify({
                "erro": "Acesso Negado", 
                "mensagem": "Você não tem permissão de Administrador para acessar esta rota."
            }), 403
        return f(*args, **kwargs)
    return decorated_function
