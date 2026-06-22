from app.utils.interfaces import InterfaceDAO
from app.utils.db import db_instance
from typing import List, Optional, Any

class UsuarioDAO(InterfaceDAO):
    """
    Classe concreta Data Access Object (DAO) para manipular os dados da entidade Usuario.
    Herda obrigatoriamente de InterfaceDAO.
    """

    def criar(self, data: dict) -> int:
        sql = """
            INSERT INTO usuarios (nome, email, senha, foto_perfil, telefone, cpf, data_nascimento)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        with self.db.cursor() as cursor:
            cursor.execute(sql, (
                data.get('nome'), 
                data.get('email'), 
                data.get('senha'), 
                data.get('foto_perfil'),
                data.get('telefone'),
                data.get('cpf'),
                data.get('data_nascimento')
            ))
            self.db.commit()
            return cursor.lastrowid

    def ler(self, id: int, **kwargs) -> Optional[dict]:
        """
        Retorna os dados do usuário a partir da sua Chave Primária (id).
        """
        sql = "SELECT id, nome, email, foto_perfil, created_at, role, status, telefone, cpf, data_nascimento FROM usuarios WHERE id = %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql, (id,))
            usuario = cursor.fetchone()
            
            # Formatação de data para o front se existir
            if usuario and usuario.get('data_nascimento'):
                usuario['data_nascimento'] = usuario['data_nascimento'].isoformat()
                
            return usuario

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

    def deletar(self, id: int, **kwargs) -> bool:
        """
        Remove um usuário do sistema em cascata.
        Limpamos as transações do usuário antes para evitar conflito de 
        RESTRICT na foreign key da categoria durante o cascade do usuário.
        """
        sql_transacoes = "DELETE FROM transacoes WHERE usuario_id = %s"
        sql_usuario = "DELETE FROM usuarios WHERE id = %s"
        with self.db.cursor() as cursor:
            cursor.execute(sql_transacoes, (id,))
            affected_rows = cursor.execute(sql_usuario, (id,))
            return affected_rows > 0

    def listar(self, **kwargs) -> List[dict]:
        """
        Lista todos os usuários. Neste exemplo não usamos filtros adicionais, 
        mas eles poderiam ser passados via kwargs.
        """
        # Trazemos o plano ativo mais recente (se houver) via JOIN
        sql = """
            SELECT u.id, u.nome, u.email, u.foto_perfil, u.created_at, u.role, u.status,
                   p.nome as plano_escolhido
            FROM usuarios u
            LEFT JOIN usuario_planos up ON u.id = up.usuario_id AND up.status = 'ativo'
            LEFT JOIN planos p ON up.plano_id = p.id
        """
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

    def atualizar_status(self, id: int, status: str) -> bool:
        """Atualiza o status de um usuário."""
        sql = "UPDATE usuarios SET status = %s WHERE id = %s"
        with self.db.cursor() as cursor:
            affected_rows = cursor.execute(sql, (status, id))
            return affected_rows > 0
