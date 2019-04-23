# -*- coding: utf-8 -*-

import requests
import json

token = 'token'

proxy = input('Usar proxy de rede? ( S - sim ou N - não) ')
log_tela = input('Gerar log em tela? ( S - sim ou N - não) ')
salvar_banco = input('Salvar dados no banco? ( S - sim ou N - não) ')
unidade_federativa = input('Buscar um ou todos? ( U - um ou T - todos) ')

if proxy == 'S':

    usuario = input('Usuario de rede: ')
    senha = input('Senha de rede: ')
    url = input('URL do proxy: ')
    porta = input('Porta do proxy: ')

    proxies = {
        'http': 'http://{0}:{1}@{2}:{3}'.format(usuario, senha, url, porta),
        'https': 'http://{0}:{1}@{2}:{3}'.format(usuario, senha, url, porta),
    }

if unidade_federativa == 'T':
    siglas_estados = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
                      "MT", "MS", "MG", "PA", "PB", "PE", "PR", "PI", "RJ", "RN",
                      "RS", "RO", "RR", "SC", "SP", "SE", "TO"]
else:
    siglas_estados = []
    siglas_estados.append(input('Digite o estado (sigla): '))

arquivo = open('localidades.sql', 'w')

for uf in siglas_estados:

    if proxy == 'S':
        resposta = requests.get('http://apiadvisor.climatempo.com.br/api/v1/locale/city?state={}&token={}'
                                .format(uf, token), proxies=proxies)
    else:
        resposta = requests.get('http://apiadvisor.climatempo.com.br/api/v1/locale/city?state={}&token={}'
                                .format(uf, token))

    lista = json.loads(resposta.text)

    for registro in lista:
        id_cidade = registro['id']
        nome = registro['name']
        estado = registro['state']

        sql = 'INSERT INTO localidades (id_cidade, nome, estado) VALUES ({0}, \'{1}\', \'{2}\');\n'\
            .format(id_cidade, nome, estado)

        if log_tela == 'S':
            print(sql)

        arquivo.write(sql)

arquivo.close()
