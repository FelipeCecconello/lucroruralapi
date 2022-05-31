from flask_restful import Resource, reqparse, inputs
from models.nota_fiscal import NotaFiscalModel
from datetime import date, datetime

class NotaFiscal(Resource):

    atributos = reqparse.RequestParser()
    atributos.add_argument('numero')
    atributos.add_argument('data')
    atributos.add_argument('nome_produto')
    atributos.add_argument('categoria')
    atributos.add_argument('quantidade')
    atributos.add_argument('valor_total')
    atributos.add_argument('fornecedor')


    def post(self):
        dados = NotaFiscal.atributos.parse_args()
        nota_fiscal = NotaFiscalModel(**dados)
        nota_fiscal.salva_nota()
        return nota_fiscal.json(), 201
