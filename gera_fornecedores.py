import requests

file = open("fornecedor.csv", "r")
endpoint_post_fornecedor = 'http://127.0.0.1:5000/fornecedor'
headers_post = {
    'Content-Type': 'application/json'
}

for linha in file:
    dados = linha.split(";")
    dados_json = {
        'fornecedor_id': '{}'.format(dados[0]),
        'nome_fornecedor': '{}'.format(dados[1]),
        'cnpj': '{}'.format(dados[2]),
        'telefone': '{}'.format(dados[3])
    }
    resposta_post = requests.request('POST', endpoint_post_fornecedor, json=dados_json, headers=headers_post)
    