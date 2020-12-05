import json
from itertools import islice
import urllib.request

import numpy as np
import pandas as pd 
import matplotlib as plt

from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier

from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import GridSearchCV


N_VIZINHOS = 5


def conecta_api():

	httpresponse = urllib.request.urlopen('https://www.dcc.ufrrj.br/ocupationdb/api.php?period_from=2019-12-06%2008:00:00&period_to=2019-12-06%2008:05:00&type=data');
	data = json.loads(httpresponse.read().decode())
	return data;


def carrega_dados(limit):

	dados = conecta_api()
	# dados = dados[1:limit]

	dataFrame =  pd.DataFrame.from_dict(dados)
	
	# print(dataFrame.head().T)
	# print(dataFrame.info())
	# print(dataFrame['mac'].value_counts())

	return dataFrame


def executa_knn(dataFrame):

	X_train, X_test, y_train, y_test = train_test_split(dataFrame.drop(['t', 'device_id', 'd'], 1), dataFrame['device_id'], test_size=0.3)

	knn = KNeighborsClassifier(n_neighbors=N_VIZINHOS) 

	print(knn.fit(X_train, y_train))

	# resultado = knn.predict([[43, -51]])
	resultado = knn.predict(X_test)

	# print(resultado)

	print (pd.crosstab(y_test,resultado, rownames=['Real'], colnames=['Predito'], margins=True))



def define_melhor_k(dataFrame):

	
	k_list = list(range(1,31))
	
	parametros = dict(n_neighbors=k_list)

	knn = KNeighborsClassifier(n_neighbors=3) 

	grid = GridSearchCV(knn, parametros, cv=5, scoring='accuracy')

	grid.fit(dataFrame.drop(['t', 'device_id', 'd'], 1), dataFrame['device_id'])
	
	print("Melhores parametros {} com o valor de acurácia {} ".format(grid.best_params_,grid.best_score_))


 
dataFrame = carrega_dados(100)

executa_knn(dataFrame)

#define_melhor_k(dataFrame)
