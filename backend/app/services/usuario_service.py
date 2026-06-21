from app.utils.interfaces import InterfaceService
from app.models.usuario_dao import UsuarioDAO
from app.models.plano_dao import PlanoDAO
from app.utils.mongo_db import registrar_login, registrar_inclusao, registrar_alteracao
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, has_request_context
import jwt
import os
import datetime

class UsuarioService(InterfaceService):
    """
    Camada de Serviço para Usuários. Contém toda a lógica de negócio,
    validações, hashes de senha e disparos para o log de auditoria no MongoDB.
    """
    def __init__(self):
        self.dao = UsuarioDAO()

    def executar_regras_negocio(self, *args, **kwargs):
        pass # Implementação genérica obrigatória da Interface base

    def criar_usuario(self, data: dict) -> dict:
        # Regra 1: Não permitir e-mails duplicados
        existente = self.dao.buscar_por_email(data.get("email"))
        if existente:
            raise ValueError("O e-mail informado já está em uso.")
            
        # Regra 2: Criptografar a senha antes de salvar
        senha_pura = data.get("senha")
        data["senha"] = generate_password_hash(senha_pura)
        
        # Acesso ao DAO
        usuario_id = self.dao.criar(data)
        
        # Atribuir plano Básico automaticamente
        plano_dao = PlanoDAO()
        planos = plano_dao.listar()
        plano_basico = next((p for p in planos if p['nome'] == 'Básico'), None)
        if plano_basico:
            plano_dao.assinar_plano(usuario_id, plano_basico['id'])
        
        # Disparo de Auditoria pro MongoDB
        data_sem_senha = data.copy()
        if "senha" in data_sem_senha:
            del data_sem_senha["senha"]
        registrar_inclusao("usuarios", usuario_id, data_sem_senha, str(usuario_id))
        
        return {"id": usuario_id, "mensagem": "Usuário cadastrado com sucesso!"}

    def realizar_login(self, email: str, senha_pura: str) -> dict:
        """Valida credenciais e gera o JWT Token."""
        usuario = self.dao.buscar_por_email(email)
        
        ip = request.remote_addr if has_request_context() else 'unknown'
        
        if not usuario or not check_password_hash(usuario['senha'], senha_pura):
            registrar_login(email, ip, False)
            raise ValueError("E-mail ou senha incorretos.")
            
        if usuario.get('status') == 'bloqueado':
            registrar_login(email, ip, False)
            raise ValueError("Sua conta foi bloqueada. Entre em contato com o suporte.")
            
        secret = os.getenv('JWT_SECRET', 'super_secret')
        # Token expira em 24h
        payload = {
            "usuario_id": usuario["id"],
            "email": usuario["email"],
            "role": usuario.get("role", "user"),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(payload, secret, algorithm="HS256")
        
        registrar_login(email, ip, True)
        
        return {
            "token": token, 
            "usuario": {
                "id": usuario["id"], 
                "nome": usuario["nome"], 
                "email": usuario["email"],
                "foto_perfil": usuario["foto_perfil"],
                "role": usuario.get("role", "user"),
                "status": usuario.get("status", "ativo")
            }
        }

    def atualizar_usuario(self, usuario_id: int, data: dict) -> dict:
        usuario_atual = self.dao.ler(usuario_id)
        if not usuario_atual:
            raise ValueError("Usuário não encontrado.")
            
        novo_email = data.get("email")
        if novo_email and novo_email != usuario_atual["email"]:
            existente = self.dao.buscar_por_email(novo_email)
            if existente:
                raise ValueError("O e-mail informado já está em uso.")
                
        usuario_completo = self.dao.buscar_por_email(usuario_atual["email"])
        senha_hash = usuario_completo["senha"]
        
        nova_senha = data.get("nova_senha")
        senha_atual = data.get("senha_atual")
        
        if nova_senha:
            if not check_password_hash(senha_hash, senha_atual):
                raise ValueError("A senha atual informada está incorreta.")
            senha_hash = generate_password_hash(nova_senha)
            
        dados_atualizados = {
            "nome": data.get("nome", usuario_atual["nome"]),
            "email": novo_email or usuario_atual["email"],
            "senha": senha_hash,
            "foto_perfil": data.get("foto_perfil", usuario_atual["foto_perfil"])
        }
        
        self.dao.atualizar(usuario_id, dados_atualizados)
        
        # Ocultar hashes de senha nos logs
        antes_log = usuario_atual.copy()
        if 'senha' in antes_log: del antes_log['senha']
        
        depois_log = dados_atualizados.copy()
        if 'senha' in depois_log: del depois_log['senha']
        
        registrar_alteracao("usuarios", usuario_id, antes_log, depois_log, str(usuario_id))
        
        return {
            "mensagem": "Perfil atualizado com sucesso!", 
            "usuario": {
                "id": usuario_id, 
                "nome": dados_atualizados["nome"], 
                "email": dados_atualizados["email"], 
                "foto_perfil": dados_atualizados["foto_perfil"],
                "role": usuario_atual.get("role", "user"),
                "status": usuario_atual.get("status", "ativo")
            }
        }
