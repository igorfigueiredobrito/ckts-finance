from abc import ABC, abstractmethod
from typing import Any, List, Optional

class InterfaceDAO(ABC):
    """
    Interface base para todos os Data Access Objects (DAOs).
    Define o contrato obrigatório para as operações de banco de dados (CRUD).
    """
    @property
    def db(self):
        from app.utils.db import db_instance
        return db_instance.get_connection()
    
    @abstractmethod
    def criar(self, data: dict) -> Any:
        """Cria um novo registro no banco de dados e retorna seu identificador ou a entidade."""
        pass

    @abstractmethod
    def ler(self, id: int) -> Optional[dict]:
        """Busca um registro específico através do seu ID."""
        pass

    @abstractmethod
    def atualizar(self, id: int, data: dict) -> bool:
        """Atualiza um registro existente, retornando True se houve sucesso."""
        pass

    @abstractmethod
    def deletar(self, id: int) -> bool:
        """Deleta (ou inativa de forma lógica) um registro, retornando True se houve sucesso."""
        pass

    @abstractmethod
    def listar(self, **kwargs) -> List[dict]:
        """Lista múltiplos registros. Pode receber parâmetros de filtro em kwargs."""
        pass

class InterfaceService(ABC):
    """
    Interface base para a camada de Serviço (Service Layer).
    Define onde as regras de negócio devem ser encapsuladas.
    """
    
    @abstractmethod
    def executar_regras_negocio(self, *args, **kwargs) -> Any:
        """Assinatura base para execução da lógica principal do serviço."""
        pass

class InterfaceController(ABC):
    """
    Interface base para a camada de Controle (Controllers/Routers).
    Define as ações necessárias para lidar com as requisições HTTP (Flask Request -> Response).
    """
    
    @abstractmethod
    def processar_requisicao(self, *args, **kwargs) -> Any:
        """Assinatura base para processamento das entradas da web."""
        pass
