from app.utils.interfaces import InterfaceService
from app.models.plano_dao import PlanoDAO
from app.utils.mongo_db import registrar_inclusao, registrar_alteracao, registrar_exclusao
import pymysql.err

class PlanoService(InterfaceService):
    def __init__(self):
        self.dao = PlanoDAO()

    def executar_regras_negocio(self, *args, **kwargs):
        pass

    def listar_planos(self):
        return self.dao.listar()

    def criar_plano(self, admin_id: int, dados: dict):
        try:
            plano_id = self.dao.criar(dados)
            registrar_inclusao("planos", plano_id, dados, str(admin_id))
            return {"mensagem": "Plano criado com sucesso.", "id": plano_id}
        except pymysql.err.IntegrityError:
            raise ValueError("Já existe um plano com este nome.")

    def atualizar_plano(self, admin_id: int, plano_id: int, dados: dict):
        plano_atual = self.dao.ler(plano_id)
        if not plano_atual:
            raise ValueError("Plano não encontrado.")
            
        try:
            sucesso = self.dao.atualizar(plano_id, dados)
            if sucesso:
                registrar_alteracao("planos", plano_id, plano_atual, dados, str(admin_id))
                return {"mensagem": "Plano atualizado com sucesso."}
            raise ValueError("Nenhum dado modificado.")
        except pymysql.err.IntegrityError:
            raise ValueError("Já existe um plano com este nome.")

    def deletar_plano(self, admin_id: int, plano_id: int):
        plano_atual = self.dao.ler(plano_id)
        if not plano_atual:
            raise ValueError("Plano não encontrado.")
            
        try:
            sucesso = self.dao.deletar(plano_id)
            if sucesso:
                registrar_exclusao("planos", plano_id, plano_atual, str(admin_id))
                return {"mensagem": "Plano excluído."}
            raise ValueError("Falha ao excluir o plano.")
        except pymysql.err.IntegrityError:
            raise ValueError("Não é possível excluir este plano pois já existem usuários com esta assinatura.")

    # --- Lógica de Assinatura (N:N) ---
    def assinar_plano(self, usuario_id: int, plano_id: int):
        plano = self.dao.ler(plano_id)
        if not plano:
            raise ValueError("O plano escolhido não existe.")
            
        sucesso = self.dao.assinar_plano(usuario_id, plano_id)
        if sucesso:
            detalhes_assinatura = {"usuario_id": usuario_id, "plano_id": plano_id, "plano_nome": plano.get("nome")}
            registrar_inclusao("usuario_planos", plano_id, detalhes_assinatura, str(usuario_id))
            return {"mensagem": f"Você agora é assinante do plano {plano.get('nome')}."}
        raise ValueError("Falha ao registrar a assinatura.")

    def minhas_assinaturas(self, usuario_id: int):
        return self.dao.listar_assinaturas_usuario(usuario_id)
