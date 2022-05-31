from flask import Flask
from flask_restful import Api
from resources.conta import Conta, Contas
from resources.nota_fiscal import NotaFiscal
from resources.fornecedor import Fornecedor
from sql_alchemy import banco
import json
from uuid import UUID
import os

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj: any) -> any:  # pylint:disable=arguments-differ
        if isinstance(obj, UUID):
            return str(obj) # <- notice I'm not returning obj.hex as the original answer
        return json.JSONEncoder.default(self, obj)


# ?: api configuration to switch the json encoder
class MyConfig(object):
    RESTFUL_JSON = {"cls": UUIDEncoder}

app = Flask(__name__)
app.config.from_object(MyConfig)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gfrophgmujolkb:195fb559e934358036bec95429b9ed32f12df5f9971ebf4e3ca5af1fc2271adc@ec2-3-234-131-8.compute-1.amazonaws.com:5432/d5u9ded7qb9f1i'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
banco.init_app(app)
api = Api(app)

@app.route('/')
def index():
    return '<h1>Bem Vindo a API!!!</h1>'

api.add_resource(Fornecedor, '/fornecedor')
api.add_resource(NotaFiscal, '/nota')
api.add_resource(Contas, '/contas')
api.add_resource(Conta, '/conta/<string:conta_id>')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)