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
data_limite =  '2021-02-27 16:35:57.677470'


dt_sala = (dataFrame[ (dataFrame['date_time'] < data_limite )])

## separar o dataframe por RP . seriam 7 dataframes

# matriz 10x3


print(dt_sala)


tuplas = dt_sala.itertuples()

obj_media = { 'sala' :  {'vetor_amostras' : [] , 'vetor_auxiliar' : []} , 'quarto' : {'vetor_amostras' : [], 'vetor_auxiliar' : []}, 'cozinha' : {'vetor_amostras' : [], 'vetor_auxiliar' : []}}

outrp = dt_sala.itertuples()
test = list(outrp)

data = datetime.strptime(test[0].date_time, "%Y-%m-%d %H:%M:%S.%f")

segundo_atual = data.second

matrizT = []

for i in tuplas:


    obj_media[i.device_id]['vetor_auxiliar'].append(i.device_signal)

    # se a data subir um minuto, fazer a média das datas acumuladas e guardar no array de amostra

    data = datetime.strptime(i.date_time, "%Y-%m-%d %H:%M:%S.%f")

    if(data.second > segundo_atual):
        
        print('sahblau')
        
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


obj_media['cozinha']['vetor_auxiliar'].clear()
obj_media['sala']['vetor_auxiliar'].clear()
obj_media['quarto']['vetor_auxiliar'].clear()


print(obj_media)


# {'device_id': 'informatica', 'mac': '129858', 's': '-59', 't': '0988', 'd': 1575630298428}

# {'PR' : 131341, 'sinal_sala' : -54. 'sinal_quarto': -97 , 'sinal_cozinha: 0'}

print(matrizT)

dataFrameT =  pd.DataFrame.from_dict(matrizT)

print(dataFrameT)