import json
from itertools import islice
import urllib.request


def conecta_api():

	httpresponse = urllib.request.urlopen('http://localhost:3333/');
	data = json.loads(httpresponse.read().decode())
	return data;


def le_arquivo_json():

	with open('data.json', 'r') as arquivoJson:
		dados = arquivoJson.read()
		obj = json.loads(data)
	return obj;


def carrega_dados(limit):

	dados = conecta_api()

	matriz = []

	for dado in dados[:limit]:
		print(dado)
		matriz.append( [ dado['device_id'], dado['mac'], dado['s'], dado['t'], dado['d'] ])
	
	return matriz




matriz_dados = carrega_dados(10)

print(matriz_dados)