from flask_restful import Resource, reqparse, inputs
from models.conta import ContaModel
from models.nota_fiscal import NotaFiscalModel

class Contas(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('fornecedor')
    atributos.add_argument('data_vencimento')
    atributos.add_argument('pago', type=inputs.boolean)
    atributos.add_argument('notas', type=list, location='json')

    def get(self):
        return {'contas': [conta.get_conta() for conta in ContaModel.query.all()]}

    def post(self):
        dados = Conta.atributos.parse_args()
        conta = ContaModel(dados['fornecedor'], dados['data_vencimento'], dados['pago'])

        for nota in dados.notas:
            nota_fiscal = NotaFiscalModel.encontra_nota(nota)
            if nota_fiscal == None:
                return {'message': 'Nota fiscal não encontrada'}, 404

            if str(dados.fornecedor) == str(nota_fiscal.fornecedor):
                conta.notas.append(nota_fiscal)
            else: 
                return {'message': 'Não é possível adicionar notas fiscais de fornecedores diferentes'}, 400   

        conta.salva_conta()
        return conta.json(), 201

class Conta(Resource):
    atributos = reqparse.RequestParser()
    atributos.add_argument('fornecedor')
    atributos.add_argument('data_vencimento')
    atributos.add_argument('pago', type=inputs.boolean)
    atributos.add_argument('notas', type=list, location='json')

    def get(self, conta_id):
        conta = ContaModel.procura_conta(conta_id)
        if conta:
            return conta.get_conta()
        return {'message': 'Conta não encontrada.'}, 404 # not found

    def put(self, conta_id):

        dados = Conta.atributos.parse_args()
        conta_encontrada = ContaModel.procura_conta(conta_id)
        if conta_encontrada:
            conta_encontrada.atualiza_conta(dados['fornecedor'], dados['data_vencimento'], dados['pago'])

            for nota in dados.notas:
                nota_fiscal = NotaFiscalModel.encontra_nota(nota)

                if str(dados.fornecedor) == str(nota_fiscal.fornecedor):
                    conta_encontrada.notas.append(nota_fiscal)
                else: 
                    return {'message': 'Não é possível adicionar notas fiscais de fornecedores diferentes'}, 400 

            conta_encontrada.salva_conta()
            return conta_encontrada.json(), 200
        return {'message': 'A conta não foi encontrada'}, 404

    def delete(self, conta_id):
        conta = ContaModel.procura_conta(conta_id)

        if conta:
            if conta.notas == []:
                conta.deleta_conta()
                return {'message': 'Conta deletada.'}
            return {'message': 'A conta possui notas fiscais vinculadas.'}, 400
        return {'message': 'Conta não encontrada.'}, 404