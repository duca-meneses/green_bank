from flask import Blueprint

health_check = Blueprint('health_check', __name__, url_prefix='/')


@health_check.route('', methods=['GET'])
def verify_health_check():
    return {'status': 'ok'}
