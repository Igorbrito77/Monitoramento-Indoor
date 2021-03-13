import pandas as pd 
import numpy as np
from datetime import datetime, timedelta

try:
    dataFrame = pd.read_csv ('pkts-tcc-igor.csv') 

except: 
    dataFrame =  pd.read_csv('pkts-tcc-igor.txt', delimiter="	") 
    dataFrame.to_csv ('pkts-tcc-igor.csv')
    dataFrame = pd.read_csv ('pkts-tcc-igor.csv')


data_inicial = '2021-02-27 16:35:51.677470'
data_limite =  '2021-02-27 16:35:52.704400'
numero_amostras = 10


dt_sala = (dataFrame[ (dataFrame['date_time'] < data_limite )]) #['date_time']
# matriz 10x3
print(dt_sala)


tuplas = dt_sala.itertuples()

obj_media = { 'sala' :  {'vetor_amostras' : [] , 'vetor_auxiliar' : []} , 'quarto' : {'vetor_amostras' : [], 'vetor_auxiliar' : []}, 'cozinha' : {'vetor_amostras' : [], 'vetor_auxiliar' : []}}

outrp = dt_sala.itertuples()
test = list(outrp)

data = datetime.strptime(test[0].date_time, "%Y-%m-%d %H:%M:%S.%f")

segundo_atual = data.second

for i in tuplas:


    obj_media[i.device_id]['vetor_auxiliar'].append(i.device_signal)

    # se a data subir um minuto, fazer a média das datas acumuladas e guardar no array de amostra

    data = datetime.strptime(i.date_time, "%Y-%m-%d %H:%M:%S.%f")

    if(data.second > segundo_atual):
        
        print('sahblau')
        
        if(len(obj_media['cozinha']['vetor_auxiliar']) == 0):
            obj_media['cozinha']['vetor_amostras'].append(0)
        else:
             obj_media['cozinha']['vetor_amostras'].append(int( sum(obj_media['cozinha']['vetor_auxiliar']) / len(obj_media['cozinha']['vetor_auxiliar'])) )

        if(len(obj_media['sala']['vetor_auxiliar']) == 0):
            obj_media['sala']['vetor_amostras'].append(0)
        else:
             obj_media['sala']['vetor_amostras'].append(int( sum(obj_media['sala']['vetor_auxiliar']) / len(obj_media['sala']['vetor_auxiliar'])) )

        if(len(obj_media['quarto']['vetor_auxiliar']) == 0):
            obj_media['quarto']['vetor_amostras'].append(0)
        else:
             obj_media['quarto']['vetor_amostras'].append(int( sum(obj_media['quarto']['vetor_auxiliar']) / len(obj_media['quarto']['vetor_auxiliar'])) )


        obj_media['cozinha']['vetor_auxiliar'].clear()
        obj_media['sala']['vetor_auxiliar'].clear()
        obj_media['quarto']['vetor_auxiliar'].clear()

        segundo_atual = data.second


# obj_media['cozinha']['vetor_auxiliar'].clear()
# obj_media['sala']['vetor_auxiliar'].clear()
# obj_media['quarto']['vetor_auxiliar'].clear()


print(obj_media)

# matriz_treino = np.array([[], [], []])



# matriz_treino = [ obj_media['sala']['vetor_amostras'] , obj_media['quarto']['vetor_amostras'], obj_media['cozinha']['vetor_amostras']   ]

# matriz_treino[0][0] = obj_media['sala']['vetor_amostras']
# matriz_treino[0][1] = obj_media['quarto']['vetor_amostras']
# matriz_treino[0][2] = obj_media['cozinha']['vetor_amostras']

# matriz_treino = np.array([])

# matriz_treino = np.column_stack((matriz_treino, obj_media['sala']['vetor_amostras']))


# print(matriz_treino)

