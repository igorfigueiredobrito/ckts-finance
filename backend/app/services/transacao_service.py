from app.utils.interfaces import InterfaceService
from app.models.transacao_dao import TransacaoDAO
from app.utils.mongo_db import registrar_auditoria

class TransacaoService(InterfaceService):
    """
    Regras de Negócio para Transações Financeiras.
    """
    def __init__(self):
        self.dao = TransacaoDAO()

    def executar_regras_negocio(self, *args, **kwargs):
        pass

    def criar_transacao(self, data: dict, usuario_id: int) -> dict:
        # Regra: Transação não pode ser negativa
        valor = float(data.get("valor", 0))
        if valor < 0:
            raise ValueError("O valor da transação não pode ser negativo.")
            
        data["usuario_id"] = usuario_id
        
        transacao_id = self.dao.criar(data)
        
        # Audita no MongoDB
        registrar_auditoria("INCLUSAO", "transacoes", transacao_id, usuario_id)
        return {"id": transacao_id, "mensagem": "Transação registrada com sucesso."}
        
    def atualizar_transacao(self, id: int, data: dict, usuario_id: int) -> dict:
        valor = float(data.get("valor", 0))
        if valor < 0:
            raise ValueError("O valor da transação não pode ser negativo.")
            
        data["usuario_id"] = usuario_id
        sucesso = self.dao.atualizar(id, data)
        
        if sucesso:
            registrar_auditoria("ALTERACAO", "transacoes", id, usuario_id)
            return {"mensagem": "Transação atualizada com sucesso."}
        else:
            raise ValueError("Transação não encontrada ou você não tem permissão para editá-la.")
        
    def deletar_transacao(self, id: int, usuario_id: int) -> dict:
        # Precisamos garantir que a transação pertença a este usuário antes de deletar
        transacao = self.dao.ler(id)
        if not transacao or transacao.get("usuario_id") != usuario_id:
             raise ValueError("Transação não encontrada ou acesso negado.")
             
        sucesso = self.dao.deletar(id)
        if sucesso:
            registrar_auditoria("EXCLUSAO", "transacoes", id, usuario_id)
            return {"mensagem": "Transação excluída com sucesso."}
        raise ValueError("Falha ao deletar a transação.")
        
    def listar_transacoes(self, usuario_id: int, **kwargs) -> list:
        return self.dao.listar(usuario_id=usuario_id, **kwargs)

    def ler_transacao(self, id: int, usuario_id: int) -> dict:
        transacao = self.dao.ler(id)
        if not transacao or transacao.get("usuario_id") != usuario_id:
            raise ValueError("Transação não encontrada ou acesso negado.")
        return transacao
