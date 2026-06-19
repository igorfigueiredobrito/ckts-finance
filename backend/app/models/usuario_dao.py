from app.utils.interfaces import InterfaceDAO
from app.utils.db import db_instance
from typing import List, Optional, Any

class UsuarioDAO(InterfaceDAO):
    """
    Classe concreta Data Access Object (DAO) para manipular os dados da entidade Usuario.
    Herda obrigatoriamente de InterfaceDAO.
    """

    def criar(self, data: dict) -> int:
        """
        Insere um novo usuário e retorna seu ID gerado automaticamente.
        """
        sql = """
            INSERT INTO usuarios (nome, email, senha, foto_perfil)
            VALUES (%s, %s, %s, %s)
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql, (
                data.get('nome'), 
                data.get('email'), 
                data.get('senha'), 
                data.get('foto_perfil')
            ))
            return cursor.lastrowid

    def ler(self, id: int) -> Optional[dict]:
        """
        Retorna os dados do usuário a partir da sua Chave Primária (id).
        """
        sql = "SELECT id, nome, email, foto_perfil, created_at FROM usuarios WHERE id = %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql, (id,))
            return cursor.fetchone()

    def atualizar(self, id: int, data: dict) -> bool:
        """
        Modifica os dados de um usuário já existente.
        """
        sql = """
            UPDATE usuarios 
            SET nome = %s, email = %s, senha = %s, foto_perfil = %s
            WHERE id = %s
        """
        with self.db.cursor() as cursor:
            affected_rows = cursor.execute(sql, (
                data.get('nome'), 
                data.get('email'), 
                data.get('senha'), 
                data.get('foto_perfil'),
                id
            ))
            return affected_rows > 0

    def deletar(self, id: int) -> bool:
        """
        Remove um usuário do sistema em cascata.
        """
        sql = "DELETE FROM usuarios WHERE id = %s"
        with self.db.cursor() as cursor:
            affected_rows = cursor.execute(sql, (id,))
            return affected_rows > 0

    def listar(self, **kwargs) -> List[dict]:
        """
        Lista todos os usuários. Neste exemplo não usamos filtros adicionais, 
        mas eles poderiam ser passados via kwargs.
        """
        sql = "SELECT id, nome, email, foto_perfil, created_at FROM usuarios"
        with self.db.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
            
    # --- Métodos extras que não estão na Interface Base mas são específicos desta DAO ---
    def buscar_por_email(self, email: str) -> Optional[dict]:
        """
        Busca um usuário exclusivamente pelo e-mail, incluindo o hash da senha.
        Utilizado principalmente no Service de Autenticação/Login.
        """
        sql = "SELECT * FROM usuarios WHERE email = %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql, (email,))
            return cursor.fetchone()
