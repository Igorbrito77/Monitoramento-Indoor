import pandas as pd 


try:
    dataFrame = pd.read_csv ('pkts-tcc-igor.csv') 

except: 
    dataFrame =  pd.read_csv('pkts-tcc-igor.txt', delimiter="	") 
    dataFrame.to_csv ('pkts-tcc-igor.csv')
    dataFrame = pd.read_csv ('pkts-tcc-igor.csv')


data_inicial = '2021-02-27 16:35:51.677470'
data_limite =  '2021-02-27 16:35:52.704400'
numero_amostras = 10


dt_sala = (dataFrame[ (dataFrame['device_id'] == 'sala') & (dataFrame['date_time'] < data_limite )]) #['date_time']



# matriz 10x3

print(dt_sala)

tuplas = dt_sala.itertuples()

vet = []
vetor_auxiliar = []

obj_media = { 'sala' : vetor_amostras : [] , 'quarto' : vetor_amostras : [], 'cozinha' : vetor_amostras : []}

for i in tuplas:

    # if(i.device_id == 'sala'):
    #     vet.append({  i.device_signal, i.date_time })

    vetor_auxiliar.append(i.device_signal)

    # se a data subir um minuto, fazer a média das datas acumuladas e guardar no array de amostra
    # vet.append(i.date_time) 

    if(len(vetor_auxiliar) > 10):
        vet.append( [ int( sum(vetor_auxiliar) / len(vetor_auxiliar) ) ] )
        vetor_auxiliar.clear()

    if(len(vet) >  50 ):
        break

print(vet)


# vet = { "sala" : {"vetor_tempo" : []}, "quarto" : {"vetor_tempo" : []}, "cozinha" : {"vetor_tempo" : []} }

# # vet = []

# # tempo_inicial = '2021-02-27 16:35:51.677470' 

# tuplas = dataFrame.itertuples()

# # tamanho = len(list(tuplas))


# for i in tuplas:

#     # if(i.device_id == 'sala'):
#     #     vet.append({  i.device_signal, i.date_time })

#     vet[i.device_id]['vetor_tempo'].append(i.date_time) 

#     if(i.date_time >  '2021-02-27 16:35:52.677470' ):
#         break


# print(vet)