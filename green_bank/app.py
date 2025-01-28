from flask import jsonify
from flask_openapi3 import Info, OpenAPI, Tag

info = Info(title='Green Bank API', version='1.0.0')
app = OpenAPI(__name__, info=info, doc_prefix='/docs')


@app.get('/', summary='Check health', tags=[Tag(name='Health Check')])
def check_heath():
    return jsonify({'status': 'ok'})

