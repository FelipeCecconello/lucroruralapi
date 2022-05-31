from sql_alchemy import banco
from sqlalchemy.dialects.postgresql import UUID
import uuid

class FornecedorModel(banco.Model):
    __tablename__ = 'fornecedores'

    fornecedor_id = banco.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome_fornecedor = banco.Column(banco.String(80))
    cnpj = banco.Column(banco.String)
    telefone = banco.Column(banco.String)

    def __init__(self, fornecedor_id, nome_fornecedor, cnpj, telefone):
        self.fornecedor_id = fornecedor_id
        self.nome_fornecedor = nome_fornecedor
        self.cnpj = cnpj
        self.telefone = telefone

    def salva_fornecedor(self):
        banco.session.add(self)
        banco.session.commit()

    def json(self):
        return {
            'fornecedor_id': self.fornecedor_id,
            'nome_fornecedor': self.nome_fornecedor,
            'cnpj': self.cnpj,
            'telefone': self.telefone
        }