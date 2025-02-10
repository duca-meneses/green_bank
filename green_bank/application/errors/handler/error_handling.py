from flask.blueprints import Blueprint
from green_bank.application.errors.green_bank_exception import GreenBankBasicException

app = Blueprint('error_handling', __name__)

@app.errorhandler(GreenBankBasicException)
def error_handling(error):
    return error.to_dict(), error.status_code