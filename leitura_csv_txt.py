import pandas as pd 
import numpy as np
from datetime import datetime, timedelta


from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import GridSearchCV

try:
    dataFrame = pd.read_csv ('pkts-tcc-igor.csv') 

except: 
    dataFrame =  pd.read_csv('pkts-tcc-igor.txt', delimiter="	") 
    dataFrame.to_csv ('pkts-tcc-igor.csv')
    dataFrame = pd.read_csv ('pkts-tcc-igor.csv')


data_limite =  '2021-02-27 16:35:61.677470'



dt_PR_1 =  (dataFrame[ (dataFrame['id_addr']  == 131341)])
dt_PR_2 =  (dataFrame[ (dataFrame['id_addr']  == 131364)])
dt_PR_3 =  (dataFrame[ (dataFrame['id_addr']  == 131402)])
dt_PR_4 =  (dataFrame[ (dataFrame['id_addr']  == 131428)])
dt_PR_5 =  (dataFrame[ (dataFrame['id_addr']  == 131451)])
dt_PR_6 =  (dataFrame[ (dataFrame['id_addr']  == 131482)])
dt_PR_7 =  (dataFrame[ (dataFrame['id_addr']  == 131717)])


array_dataframes = [dt_PR_1, dt_PR_2, dt_PR_3, dt_PR_4, dt_PR_5, dt_PR_6, dt_PR_7]

# print(array_dataframes)

obj_media = { 'sala' :  {'vetor_amostras' : [] , 'vetor_auxiliar' : []} , 'quarto' : {'vetor_amostras' : [], 'vetor_auxiliar' : []}, 'cozinha' : {'vetor_amostras' : [], 'vetor_auxiliar' : []}}

matrizT = []

for dtFrame in array_dataframes: 

    tuplas = dtFrame.itertuples()

    outrp = dtFrame.itertuples()
    test = list(outrp)
    data = datetime.strptime(test[0].date_time, "%Y-%m-%d %H:%M:%S.%f")

    segundo_atual = data.second

    obj_media['cozinha']['vetor_auxiliar'].clear()
    obj_media['sala']['vetor_auxiliar'].clear()
    obj_media['quarto']['vetor_auxiliar'].clear()

    limite_amostras = 0

    for i in tuplas:

        obj_media[i.device_id]['vetor_auxiliar'].append(i.device_signal)

        # se a data subir um minuto, fazer a média das datas acumuladas e guardar no array de amostra
        data = datetime.strptime(i.date_time, "%Y-%m-%d %H:%M:%S.%f")

        if(data.second > segundo_atual):
                        
            vetorBi = []

            if(len(obj_media['cozinha']['vetor_auxiliar']) == 0):
                vetorBi.append(0)
            else:
                vetorBi.append(int( sum(obj_media['cozinha']['vetor_auxiliar']) / len(obj_media['cozinha']['vetor_auxiliar'])) )

            if(len(obj_media['sala']['vetor_auxiliar']) == 0):
                vetorBi.append(0)
            else:
                vetorBi.append(int( sum(obj_media['sala']['vetor_auxiliar']) / len(obj_media['sala']['vetor_auxiliar'])) )

            if(len(obj_media['quarto']['vetor_auxiliar']) == 0):
                vetorBi.append(0)
            else:
                vetorBi.append(int( sum(obj_media['quarto']['vetor_auxiliar']) / len(obj_media['quarto']['vetor_auxiliar'])) )

            matrizT.append({'PR': i.id_addr, 'sinal_cozinha' : vetorBi[0], 'sinal_sala': vetorBi[1] , 'sinal_quarto': vetorBi[2]  })


            obj_media['cozinha']['vetor_auxiliar'].clear()
            obj_media['sala']['vetor_auxiliar'].clear()
            obj_media['quarto']['vetor_auxiliar'].clear()

            segundo_atual = data.second
            limite_amostras +=1

        if(limite_amostras == 7):
            break
            
   


print(obj_media)


# {'PR' : 131341, 'sinal_sala' : -54. 'sinal_quarto': -97 , 'sinal_cozinha: 0'}

print(matrizT)

dataFrameT =  pd.DataFrame.from_dict(matrizT)

print(dataFrameT)

dataFrameT.to_csv('treinamento.csv')


X_train, X_test, y_train, y_test = train_test_split(dataFrameT.drop(['PR'], 1), dataFrameT['PR'], test_size=0.3)

print (X_train)

print(X_test)

knn = KNeighborsClassifier(n_neighbors=3) 

print(knn.fit(X_train, y_train))

# resultado = knn.predict([[43, -51]])
resultado = knn.predict(X_test)

# print(resultado)

print (pd.crosstab(y_test,resultado, rownames=['Real'], colnames=['Predito'], margins=True))
