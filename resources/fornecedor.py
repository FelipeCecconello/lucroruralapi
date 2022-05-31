from flask_restful import Resource, reqparse
from models.fornecedor import FornecedorModel

class Fornecedor(Resource):

    atributos = reqparse.RequestParser()
    atributos.add_argument('fornecedor_id')
    atributos.add_argument('nome_fornecedor')
    atributos.add_argument('cnpj')
    atributos.add_argument('telefone')

    def post(self):
        dados = Fornecedor.atributos.parse_args()
        fornecedor = FornecedorModel(**dados)
        fornecedor.salva_fornecedor()
        return fornecedor.json(), 201
