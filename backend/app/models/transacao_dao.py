from app.utils.interfaces import InterfaceDAO
from app.utils.db import db_instance
from typing import List, Optional, Any

class TransacaoDAO(InterfaceDAO):
    """
    Data Access Object (DAO) responsável pela tabela de transações.
    Acompanha os registros financeiros do usuário com relacionamento direto à Categoria.
    """

    def criar(self, data: dict) -> int:
        """
        Registra uma nova transação financeira no MySQL.
        """
        sql = """
            INSERT INTO transacoes (descricao, valor, data, usuario_id, categoria_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql, (
                data.get('descricao'), 
                data.get('valor'), 
                data.get('data'), 
                data.get('usuario_id'),
                data.get('categoria_id')
            ))
            return cursor.lastrowid

    def ler(self, id: int) -> Optional[dict]:
        """
        Lê uma transação específica e já faz o JOIN (Eager Loading manual)
        para pegar o nome e o tipo da categoria que a transação pertence.
        """
        sql = """
            SELECT t.*, c.nome as categoria_nome, c.tipo as categoria_tipo
            FROM transacoes t
            LEFT JOIN categorias c ON t.categoria_id = c.id
            WHERE t.id = %s
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql, (id,))
            return cursor.fetchone()

    def atualizar(self, id: int, data: dict) -> bool:
        """
        Atualiza uma transação. A clausula verifica o 'usuario_id' por segurança 
        para garantir que ninguém modifique transações de outra pessoa acidentalmente (IDOR).
        """
        sql = """
            UPDATE transacoes 
            SET descricao = %s, valor = %s, data = %s, categoria_id = %s
            WHERE id = %s AND usuario_id = %s
        """
        with self.db.cursor() as cursor:
            affected_rows = cursor.execute(sql, (
                data.get('descricao'), 
                data.get('valor'), 
                data.get('data'), 
                data.get('categoria_id'),
                id,
                data.get('usuario_id')
            ))
            return affected_rows > 0

    def deletar(self, id: int) -> bool:
        """
        Deleta de forma permanente a transação.
        """
        sql = "DELETE FROM transacoes WHERE id = %s"
        with self.db.cursor() as cursor:
            affected_rows = cursor.execute(sql, (id,))
            return affected_rows > 0

    def listar(self, **kwargs) -> List[dict]:
        """
        Lista todas as transações com filtros opcionais.
        """
        usuario_id = kwargs.get('usuario_id')
        descricao = kwargs.get('descricao')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        
        sql = """
            SELECT t.*, c.nome as categoria_nome, c.tipo as categoria_tipo
            FROM transacoes t
            LEFT JOIN categorias c ON t.categoria_id = c.id
            WHERE 1=1
        """
        params = []
        
        if usuario_id:
            sql += " AND t.usuario_id = %s"
            params.append(usuario_id)
            
        if descricao:
            sql += " AND t.descricao LIKE %s"
            params.append(f"%{descricao}%")
            
        if start_date:
            sql += " AND t.data >= %s"
            params.append(start_date)
            
        if end_date:
            sql += " AND t.data <= %s"
            params.append(end_date)
            
        sql += " ORDER BY t.data DESC"
        
        with self.db.cursor() as cursor:
            cursor.execute(sql, tuple(params))
            return cursor.fetchall()
