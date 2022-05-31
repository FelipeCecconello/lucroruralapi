import requests

file = open("notafiscal.csv", "r")
endpoint_post_fornecedor = 'http://127.0.0.1:5000/nota'
headers_post = {
    'Content-Type': 'application/json'
}

for linha in file:
    dados = linha.split(";")
    dados_json = {
        "numero": "{}".format(dados[0]),
        "data": "{}".format(dados[2]),
        "nome_produto": "{}".format(dados[3]),
        "categoria": "{}".format(dados[4]),
        "quantidade": "{}".format(dados[5]),
        "valor_total": "{}".format(dados[6]),
        "fornecedor": "{}".format(dados[1])
    }
    resposta_post = requests.request('POST', endpoint_post_fornecedor, json=dados_json, headers=headers_post)
    