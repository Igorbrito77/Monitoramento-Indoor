import json
from itertools import islice
import urllib.request

import numpy as np
import pandas as pd 
import matplotlib

from sklearn.cluster import KMeans


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
		# matriz.append( [ dado['device_id'], dado['mac'], dado['s'], dado['t'], dado['d'] ])
		matriz.append( [ dado['d'] ])

	
	return matriz


def executa_kmeans(matriz_dados):
	
	print(matriz_dados)
	
	kmeans = KMeans(n_clusters = 3, init = 'random')

	print( kmeans.fit(matriz_dados) )

	print ('Klusters selecionados: \n' , kmeans.cluster_centers_ )




matriz_dados = carrega_dados(10)

executa_kmeans(matriz_dados)
