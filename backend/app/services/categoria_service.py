from app.utils.interfaces import InterfaceService
from app.models.categoria_dao import CategoriaDAO
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
        return {"mensagem": "Categoria criada com sucesso", "id": novo_id}

    def atualizar_categoria(self, categoria_id: int, usuario_id: int, dados: dict) -> dict:
        cat_atual = self.dao.ler(categoria_id)
        if not cat_atual or cat_atual['usuario_id'] != usuario_id:
            raise ValueError("Categoria não encontrada ou acesso negado.")
            
        dados['usuario_id'] = usuario_id
        sucesso = self.dao.atualizar(categoria_id, dados)
        if sucesso:
            return {"mensagem": "Categoria atualizada."}
        raise ValueError("Falha ao atualizar categoria.")

    def deletar_categoria(self, categoria_id: int, usuario_id: int) -> dict:
        cat_atual = self.dao.ler(categoria_id)
        if not cat_atual or cat_atual['usuario_id'] != usuario_id:
            raise ValueError("Categoria não encontrada ou acesso negado.")
            
        try:
            sucesso = self.dao.deletar(categoria_id, usuario_id)
            if sucesso:
                return {"mensagem": "Categoria excluída com sucesso."}
            raise ValueError("Falha ao deletar categoria.")
        except pymysql.err.IntegrityError:
            raise ValueError("Não é possível excluir esta categoria pois há transações atreladas a ela.")
