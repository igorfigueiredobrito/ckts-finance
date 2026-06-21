from app.utils.interfaces import InterfaceDAO
from app.utils.db import db_instance
from typing import List, Optional, Any

class PlanoDAO(InterfaceDAO):
    """
    Data Access Object para a tabela 'planos' e a intermediária 'usuario_planos'.
    """

    def criar(self, data: dict) -> int:
        sql = "INSERT INTO planos (nome, preco, descricao) VALUES (%s, %s, %s)"
        with self.db.cursor() as cursor:
            cursor.execute(sql, (
                data.get('nome'), 
                data.get('preco'), 
                data.get('descricao')
            ))
            self.db.commit()
            return cursor.lastrowid

    def ler(self, id: int, **kwargs) -> Optional[dict]:
        sql = "SELECT id, nome, preco, descricao, created_at FROM planos WHERE id = %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql, (id,))
            return cursor.fetchone()

    def atualizar(self, id: int, data: dict) -> bool:
        sql = "UPDATE planos SET nome = %s, preco = %s, descricao = %s WHERE id = %s"
        with self.db.cursor() as cursor:
            affected_rows = cursor.execute(sql, (
                data.get('nome'), 
                data.get('preco'), 
                data.get('descricao'),
                id
            ))
            self.db.commit()
            return affected_rows > 0

    def deletar(self, id: int, **kwargs) -> bool:
        sql = "DELETE FROM planos WHERE id = %s"
        with self.db.cursor() as cursor:
            affected_rows = cursor.execute(sql, (id,))
            self.db.commit()
            return affected_rows > 0

    def listar(self, **kwargs) -> List[dict]:
        sql = "SELECT id, nome, preco, descricao, created_at FROM planos"
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
            
    # --- Relacionamento N:N ---
    def assinar_plano(self, usuario_id: int, plano_id: int) -> bool:
        """
        Insere ou reativa uma assinatura na tabela intermediária usuario_planos.
        Se o usuário já teve o plano antes, usa ON DUPLICATE KEY UPDATE para reativar.
        """
        sql_inativar = "UPDATE usuario_planos SET status = 'cancelado' WHERE usuario_id = %s"
        sql_assinar = """
            INSERT INTO usuario_planos (usuario_id, plano_id, status)
            VALUES (%s, %s, 'ativo')
            ON DUPLICATE KEY UPDATE status = 'ativo', data_assinatura = CURRENT_TIMESTAMP
        """
        with self.db.cursor() as cursor:
            # Primeiro inativa qualquer assinatura ativa
            cursor.execute(sql_inativar, (usuario_id,))
            # Depois insere/reativa o novo plano
            affected_rows = cursor.execute(sql_assinar, (usuario_id, plano_id))
            self.db.commit()
            return affected_rows > 0

    def listar_assinaturas_usuario(self, usuario_id: int) -> List[dict]:
        sql = """
            SELECT p.id, p.nome, p.preco, p.descricao, up.status, up.data_assinatura
            FROM planos p
            JOIN usuario_planos up ON p.id = up.plano_id
            WHERE up.usuario_id = %s
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql, (usuario_id,))
            return cursor.fetchall()
