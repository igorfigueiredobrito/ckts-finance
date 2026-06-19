from app.utils.interfaces import InterfaceDAO
from app.utils.db import db_instance
from typing import List, Optional

class CategoriaDAO(InterfaceDAO):
    """
    Data Access Object para a tabela categorias.
    """

    def criar(self, data: dict) -> int:
        sql = "INSERT INTO categorias (nome, tipo, usuario_id) VALUES (%s, %s, %s)"
        with self.db.cursor() as cursor:
            cursor.execute(sql, (data.get('nome'), data.get('tipo'), data.get('usuario_id')))
            return cursor.lastrowid

    def ler(self, id: int) -> Optional[dict]:
        sql = "SELECT id, nome, tipo, usuario_id FROM categorias WHERE id = %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql, (id,))
            return cursor.fetchone()

    def atualizar(self, id: int, data: dict) -> bool:
        sql = "UPDATE categorias SET nome = %s, tipo = %s WHERE id = %s AND usuario_id = %s"
        with self.db.cursor() as cursor:
            affected = cursor.execute(sql, (data.get('nome'), data.get('tipo'), id, data.get('usuario_id')))
            return affected > 0

    def deletar(self, id: int, usuario_id: int) -> bool:
        sql = "DELETE FROM categorias WHERE id = %s AND usuario_id = %s"
        with self.db.cursor() as cursor:
            affected = cursor.execute(sql, (id, usuario_id))
            return affected > 0

    def listar(self, **kwargs) -> List[dict]:
        """
        Lista todas as categorias pertencentes ao usuário logado.
        """
        usuario_id = kwargs.get('usuario_id')
        sql = "SELECT id, nome, tipo FROM categorias WHERE usuario_id = %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql, (usuario_id,))
            return cursor.fetchall()
