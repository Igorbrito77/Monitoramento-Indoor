import json
from itertools import islice
import urllib.request

import numpy as np
import pandas as pd 
import matplotlib as plt

from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier

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

	dataFrame =  pd.DataFrame.from_dict(dados)

	classes = np.array(dataFrame.device_id);

	matriz = []
	for dado in dados:
		matriz.append( [float(dado['s']),  float(dado['d']) ])
		
	# print(np.array(dataFrame.drop( ['device_id','mac', 't'],  1)))

	return matriz, classes
	# return  np.array(dataFrame.drop( ['device_id', 's','mac', 't'],  1)), classes

	
def executa_kmeans(matriz_dados):
		
	kmeans = KMeans(n_clusters = 3, init = 'random')

	print( kmeans.fit(matriz_dados) )

	print ('Klusters selecionados: \n' , kmeans.cluster_centers_ )



def executa_knn(matriz_dados, classes):

	knn = KNeighborsClassifier(n_neighbors=3) 

	print(knn.fit(matriz_dados, classes))

	print(knn.predict([[-59, 1575630298428]]))





 
matriz_dados, classes = carrega_dados(10)


executa_knn(matriz_dados, classes)

