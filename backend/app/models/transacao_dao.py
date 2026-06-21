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

    def ler(self, id: int, **kwargs) -> Optional[dict]:
        """
        Lê uma transação específica e já faz o JOIN (Eager Loading manual)
        para pegar o nome e o tipo da categoria que a transação pertence.
        """
        usuario_id = kwargs.get('usuario_id')
        sql = """
            SELECT t.*, c.nome as categoria_nome, c.tipo as categoria_tipo
            FROM transacoes t
            LEFT JOIN categorias c ON t.categoria_id = c.id
            WHERE t.id = %s
        """
        params = [id]
        if usuario_id:
            sql += " AND t.usuario_id = %s"
            params.append(usuario_id)
            
        with self.db.cursor() as cursor:
            cursor.execute(sql, tuple(params))
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

    def deletar(self, id: int, **kwargs) -> bool:
        """
        Deleta de forma permanente a transação.
        """
        usuario_id = kwargs.get('usuario_id')
        sql = "DELETE FROM transacoes WHERE id = %s"
        params = [id]
        if usuario_id:
            sql += " AND usuario_id = %s"
            params.append(usuario_id)
            
        with self.db.cursor() as cursor:
            affected_rows = cursor.execute(sql, tuple(params))
            return affected_rows > 0

    def deletar_todas(self, usuario_id: int) -> int:
        """
        Deleta de forma permanente todas as transações de um usuário.
        """
        sql = "DELETE FROM transacoes WHERE usuario_id = %s"
        with self.db.cursor() as cursor:
            affected_rows = cursor.execute(sql, (usuario_id,))
            return affected_rows

    def listar(self, **kwargs) -> List[dict]:
        """
        Lista todas as transações com filtros opcionais.
        """
        usuario_id = kwargs.get('usuario_id')
        descricao = kwargs.get('descricao')
        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        min_valor = kwargs.get('min_valor')
        max_valor = kwargs.get('max_valor')
        categoria_id = kwargs.get('categoria_id')
        tipo = kwargs.get('tipo')
        
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
            
        if min_valor:
            sql += " AND t.valor >= %s"
            params.append(min_valor)
            
        if max_valor:
            sql += " AND t.valor <= %s"
            params.append(max_valor)
            
        if categoria_id:
            sql += " AND t.categoria_id = %s"
            params.append(categoria_id)
            
        if tipo:
            sql += " AND c.tipo = %s"
            params.append(tipo)
            
        sql += " ORDER BY t.data DESC"
        
        with self.db.cursor() as cursor:
            cursor.execute(sql, tuple(params))
            return cursor.fetchall()
