import pandas as pd 


try:
    dataFrame = pd.read_csv ('pkts-tcc-igor.csv') 

except: 
    dataFrame =  pd.read_csv('pkts-tcc-igor.txt', delimiter="	") 
    dataFrame.to_csv ('pkts-tcc-igor.csv')
    dataFrame = pd.read_csv ('pkts-tcc-igor.csv')



# print(dataFrame.count())


# vet = { "sala" : {"vetor_tempo" : []}, "quarto" : {"vetor_tempo" : []}, "cozinha" : {"vetor_tempo" : []} }

vet = []

# tempo_inicial = '2021-02-27 19:50:08.376471' 

tuplas = dataFrame.itertuples()

# tamanho = len(list(tuplas))


for i in tuplas:

    if(i.device_id == 'sala'):
        vet.append({  i.device_signal, i.date_time })

    if(len(vet)== 20):
        break


print(vet)