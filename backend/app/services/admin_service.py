from app.utils.interfaces import InterfaceService
from app.models.usuario_dao import UsuarioDAO
from app.utils.mongo_db import registrar_alteracao
from flask import g

class AdminService(InterfaceService):
    def __init__(self):
        self.usuario_dao = UsuarioDAO()

    def executar_regras_negocio(self, *args, **kwargs):
        pass

    def listar_usuarios(self):
        usuarios = self.usuario_dao.listar()
        return usuarios

    def alternar_status_usuario(self, id: int):
        usuario = self.usuario_dao.buscar_por_email(self.usuario_dao.ler(id).get('email'))
        if not usuario:
            raise ValueError("Usuário não encontrado.")
            
        if usuario.get('role') == 'admin':
            raise ValueError("Não é possível alterar o status de um administrador.")

        novo_status = 'bloqueado' if usuario.get('status') == 'ativo' else 'ativo'
        
        self.usuario_dao.atualizar_status(id, novo_status)
            
        # Log da alteração
        usuario_depois = usuario.copy()
        usuario_depois['status'] = novo_status
        admin_id = getattr(g, 'usuario_id', 'admin_desconhecido')
        registrar_alteracao("usuarios", id, usuario, usuario_depois, str(admin_id))
            
        return {"mensagem": f"Status do usuário alterado para {novo_status}.", "status": novo_status}

    def estatisticas_gerais(self):
        usuarios = self.usuario_dao.listar()
        
        ativos = [u for u in usuarios if u.get('status') == 'ativo']
        total_ativos = len(ativos)
        
        from app.models.plano_dao import PlanoDAO
        plano_dao = PlanoDAO()
        planos = plano_dao.listar()
        
        tabela_precos = {p['nome']: float(p['preco']) for p in planos}
        distribuicao_planos = {p['nome']: 0 for p in planos}
        
        mrr = 0
        
        for u in ativos:
            plano = u.get('plano_escolhido')
            if plano and plano in distribuicao_planos:
                distribuicao_planos[plano] += 1
                mrr += tabela_precos.get(plano, 0)
        
        return {
            "total_usuarios": len(usuarios),
            "usuarios_ativos": total_ativos,
            "usuarios_bloqueados": len(usuarios) - total_ativos,
            "mrr_estimado": mrr,
            "planos": distribuicao_planos
        }

    def deletar_usuario(self, id: int):
        from app.utils.mongo_db import registrar_exclusao
        
        usuario = self.usuario_dao.ler(id)
        if not usuario:
            raise ValueError("Usuário não encontrado.")
            
        if usuario.get('role') == 'admin':
            raise ValueError("Não é possível excluir um administrador.")
            
        sucesso = self.usuario_dao.deletar(id)
        if sucesso:
            admin_id = getattr(g, 'usuario_id', 'admin_desconhecido')
            registrar_exclusao("usuarios", id, usuario, str(admin_id))
            return {"mensagem": "Usuário excluído com sucesso."}
        else:
            raise ValueError("Falha ao excluir o usuário.")


