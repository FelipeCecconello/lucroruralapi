from sql_alchemy import banco
from sqlalchemy.dialects.postgresql import UUID
import uuid
from models.nota_fiscal import NotaFiscalModel

notas_identifier = banco.Table('notas_identifier',
    banco.Column('nota_fiscal_id', UUID(as_uuid=True), banco.ForeignKey('nota_fiscal.nota_fiscal_id')),
    banco.Column('conta_id', UUID(as_uuid=True), banco.ForeignKey('contas.conta_id'))
)

class ContaModel(banco.Model):
    __tablename__ = 'contas'

    conta_id = banco.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fornecedor = banco.Column(UUID(as_uuid=True), banco.ForeignKey('fornecedores.fornecedor_id'))
    data_vencimento = banco.Column(banco.String)
    pago = banco.Column(banco.Boolean)
    notas = banco.relationship('NotaFiscalModel', secondary=notas_identifier)

    def __init__(self, fornecedor, data_vencimento, pago):
        self.fornecedor = fornecedor
        self.data_vencimento = data_vencimento
        self.pago = pago

    def salva_conta(self):
        banco.session.add(self)
        banco.session.commit()

    def json(self):
        return {
            'conta_id': self.conta_id,
            'fornecedor': self.fornecedor,
            'data_vencimento':self.data_vencimento,
            'pago':self.pago, 
            'notas':[nota.json() for nota in self.notas]
        }
    
    def atualiza_conta(self, fornecedor, data_vencimento, pago):
        self.fornecedor = fornecedor
        self.data_vencimento = data_vencimento
        self.pago = pago
        self.notas = []
        
    @classmethod
    def procura_conta(cls, conta_id):
        conta = cls.query.filter_by(conta_id=conta_id).first()
        if conta:
            return conta
        return None

    def deleta_conta(self):
        banco.session.delete(self)
        banco.session.commit()

    def get_conta(self):
        
        valor_total = 0
        for nota in self.notas:
            valor_total += nota.valor_total

        return {
            'conta_id': self.conta_id,
            'fornecedor': self.fornecedor,
            'data_vencimento':self.data_vencimento,
            'pago':self.pago,
            'valor total': '{:.2f}'.format(valor_total)
        }