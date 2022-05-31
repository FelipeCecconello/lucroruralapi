from sql_alchemy import banco
from sqlalchemy.dialects.postgresql import UUID
import uuid

class NotaFiscalModel(banco.Model):
    __tablename__ = 'nota_fiscal'

    nota_fiscal_id = banco.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero = banco.Column(banco.Integer)
    data = banco.Column(banco.String)
    nome_produto = banco.Column(banco.String)
    categoria = banco.Column(banco.String)
    quantidade = banco.Column(banco.Float(precision=2))
    valor_total = banco.Column(banco.Float(precision=2))
    fornecedor = banco.Column(UUID(as_uuid=True), banco.ForeignKey('fornecedores.fornecedor_id'))

    def __init__(self, numero, data, nome_produto, categoria, quantidade, valor_total, fornecedor):
        self.numero = numero
        self.data = data
        self.nome_produto = nome_produto
        self.categoria = categoria
        self.quantidade = quantidade
        self.valor_total = valor_total
        self.fornecedor = fornecedor

    def salva_nota(self):
        banco.session.add(self)
        banco.session.commit()

    def json(self):
        return {
            'nota_fiscal_id': self.nota_fiscal_id,
            'numero': self.numero,
            'data':self.data,
            'nome_produto':self.nome_produto, 
            'categoria':self.categoria,
            'quantidade':self.quantidade,
            'valor_total':self.valor_total,
            'fornecedor':self.fornecedor 
        }

    @classmethod
    def encontra_nota(cls, nota_fiscal_id):
        site = cls.query.filter_by(nota_fiscal_id=nota_fiscal_id).first()
        if site:
            return site
        return None