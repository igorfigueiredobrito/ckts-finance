from flask import Blueprint
from app.controllers.data_controller import DataController
from app.middlewares.auth_middleware import jwt_required

bp_data = Blueprint('data', __name__, url_prefix='/api/data')
controller = DataController()

@bp_data.route('/export/transacoes/json', methods=['GET'])
@jwt_required
def exportar_json():
    """Baixa o JSON de todas as transações do usuário logado."""
    return controller.exportar_json()

@bp_data.route('/import/transacoes/json', methods=['POST'])
@jwt_required
def importar_json():
    """Recebe upload (multipart) de um arquivo .json para importação em lote."""
    return controller.importar_json()

@bp_data.route('/export/logs/xml', methods=['GET'])
@jwt_required
def exportar_xml():
    """Baixa o arquivo XML estruturado dos logs salvos no MongoDB."""
    return controller.exportar_xml_logs()
