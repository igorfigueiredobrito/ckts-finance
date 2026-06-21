from flask import Flask
from flask_cors import CORS
from app.middlewares.error_middleware import register_error_handlers
from app.middlewares.log_middleware import register_log_middleware
from app.routes.usuario_routes import UsuarioRouter
from app.routes.transacao_routes import TransacaoRouter
from app.routes.data_routes import DataRouter
from app.routes.categoria_routes import CategoriaRouter
from app.routes.admin_routes import AdminRouter
from app.routes.log_routes import LogRouter
from app.routes.plano_routes import PlanoRouter
from app.routes.assinatura_routes import AssinaturaRouter

def create_app():
    """
    Application Factory do Flask.
    Ideal para isolamento de testes e inicialização limpa.
    """
    app = Flask(__name__)
    CORS(app) # Libera acesso cross-origin para o Frontend Vue
    
    # 1. Registra os Middlewares Globais
    register_error_handlers(app)  # Exceções globais logadas no Mongo
    register_log_middleware(app)  # Analytics de Request logadas no Mongo
    
    # 2. Registra os Routers (Blueprints)
    app.register_blueprint(UsuarioRouter().bp)
    app.register_blueprint(TransacaoRouter().bp)
    app.register_blueprint(DataRouter().bp)
    app.register_blueprint(CategoriaRouter().bp)
    app.register_blueprint(AdminRouter().bp)
    app.register_blueprint(LogRouter().bp)
    app.register_blueprint(PlanoRouter().bp)
    app.register_blueprint(AssinaturaRouter().bp)
    
    # Rota raiz de health-check
    @app.route('/')
    def index():
        return {"status": "ok", "mensagem": "API de Controle Financeiro rodando!"}
        
    return app
