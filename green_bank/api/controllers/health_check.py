from flask import Blueprint

from green_bank.application.schemas.message import HealthCheckSchema

hc = Blueprint('health_check', __name__, url_prefix='/')


@hc.route('', methods=['GET'])
def verify_health_check():
    ''' Health Check
    ---
    get:
      tags:
        - health check
      summary: Health Check of application
      description: Health Check of application
      responses:
        200:
          description: api is running
          content:
            application/json:
              schema: HealthCheckSchema
    '''
    return HealthCheckSchema().dump({"status": "Green Bank API is running"}), 200
