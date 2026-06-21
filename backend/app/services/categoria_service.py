from app.utils.interfaces import InterfaceService
from app.models.categoria_dao import CategoriaDAO
from app.utils.mongo_db import registrar_inclusao, registrar_alteracao, registrar_exclusao
import pymysql.err

class CategoriaService(InterfaceService):
    """
    Serviço para busca e processamento de Categorias.
    """
    def __init__(self):
        self.dao = CategoriaDAO()

    def executar_regras_negocio(self, *args, **kwargs):
        pass
        
    def listar_categorias_usuario(self, usuario_id: int) -> list:
        categorias = self.dao.listar(usuario_id=usuario_id)
        return categorias

    def criar_categoria(self, usuario_id: int, dados: dict) -> dict:
        dados['usuario_id'] = usuario_id
        novo_id = self.dao.criar(dados)
        registrar_inclusao("categorias", novo_id, dados, str(usuario_id))
        return {"mensagem": "Categoria criada com sucesso", "id": novo_id}

    def atualizar_categoria(self, categoria_id: int, usuario_id: int, dados: dict) -> dict:
        cat_atual = self.dao.ler(categoria_id, usuario_id=usuario_id)
        if not cat_atual:
            raise ValueError("Categoria não encontrada ou acesso negado.")
            
        dados['usuario_id'] = usuario_id
        sucesso = self.dao.atualizar(categoria_id, dados)
        if sucesso:
            registrar_alteracao("categorias", categoria_id, cat_atual, dados, str(usuario_id))
            return {"mensagem": "Categoria atualizada."}
        raise ValueError("Falha ao atualizar categoria.")

    def deletar_categoria(self, categoria_id: int, usuario_id: int) -> dict:
        cat_atual = self.dao.ler(categoria_id, usuario_id=usuario_id)
        if not cat_atual:
            raise ValueError("Categoria não encontrada ou acesso negado.")
            
        try:
            sucesso = self.dao.deletar(categoria_id, usuario_id=usuario_id)
            if sucesso:
                registrar_exclusao("categorias", categoria_id, cat_atual, str(usuario_id))
                return {"mensagem": "Categoria excluída com sucesso."}
            raise ValueError("Falha ao deletar categoria.")
        except pymysql.err.IntegrityError:
            raise ValueError("Não é possível excluir esta categoria pois há transações atreladas a ela.")
