import pymysql
import pymysql.cursors
import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

class DatabaseHelper:
    """
    Implementação do padrão Singleton para gerenciar a conexão com o banco de dados MySQL.
    Garante que a aplicação não abra múltiplas instâncias de conexão de forma desnecessária,
    otimizando a performance.
    """
    _instance = None

    def __new__(cls):
        # Valida se a instância já existe (Singleton)
        if cls._instance is None:
            cls._instance = super(DatabaseHelper, cls).__new__(cls)
            cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        """Busca as credenciais nas variáveis de ambiente e prepara a configuração."""
        self.host = os.getenv('DB_HOST', 'localhost')
        self.user = os.getenv('DB_USER', 'root')
        self.password = os.getenv('DB_PASSWORD', '')
        self.database = os.getenv('DB_NAME', 'finance_system')
        self.port = int(os.getenv('DB_PORT', 3306))
        self.connection = None

    def get_connection(self):
        """
        Retorna a conexão ativa com o banco.
        Se a conexão estiver fechada ou inexistente, cria uma nova.
        """
        # Verifica se não temos conexão ou se a existente caiu
        if not self.connection or not self.connection.open:
            try:
                self.connection = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port,
                    cursorclass=pymysql.cursors.DictCursor,
                    autocommit=True 
                )
            except Exception as e:
                print(f"Erro ao conectar ao BD: {e}")
                raise e
        else:
            try:
                self.connection.ping(reconnect=True)
            except Exception as e:
                print(f"Erro ao pingar BD: {e}")
        return self.connection

# Instanciamos o Helper que será importado pelas classes DAO
db_instance = DatabaseHelper()
