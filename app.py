from flask import Flask
from flask_restful import Api
from resources.conta import Conta, Contas
from resources.nota_fiscal import NotaFiscal
from resources.fornecedor import Fornecedor
from sql_alchemy import banco
import json
from uuid import UUID

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
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://vtcbmzyisipnfr:4b10a3e522810e078e866429a4bc97f8367bdfe13c16b2b3f5ca317e994ee113@ec2-44-196-174-238.compute-1.amazonaws.com:5432/dagtnujslhn4op'
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
