import pandas as pd 
import numpy as np
from datetime import datetime, timedelta


from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.model_selection import GridSearchCV


def abrir_arquivo():

    try:
        dataFrame = pd.read_csv ('pkts-tcc-igor.csv') 

    except: 
        dataFrame =  pd.read_csv('pkts-tcc-igor.txt', delimiter="	") 
        dataFrame.to_csv ('pkts-tcc-igor.csv')
        dataFrame = pd.read_csv ('pkts-tcc-igor.csv')

    return dataFrame


def montar_matriz_amostras(dataFrame):

    ## separa o dataframe em partes, sendo que cada parte corresponde às leituras de sinal correspondentes a um Ponto de Referência específico
    dt_PR_1 =  (dataFrame[ (dataFrame['id_addr']  == 131341)])
    dt_PR_2 =  (dataFrame[ (dataFrame['id_addr']  == 131364)])
    dt_PR_3 =  (dataFrame[ (dataFrame['id_addr']  == 131402)])
    dt_PR_4 =  (dataFrame[ (dataFrame['id_addr']  == 131428)])
    dt_PR_5 =  (dataFrame[ (dataFrame['id_addr']  == 131451)])
    dt_PR_6 =  (dataFrame[ (dataFrame['id_addr']  == 131482)])
    dt_PR_7 =  (dataFrame[ (dataFrame['id_addr']  == 131717)])

    array_dataframes = [dt_PR_1, dt_PR_2, dt_PR_3, dt_PR_4, dt_PR_5, dt_PR_6, dt_PR_7] # cria um array contendo os dataframes de cada Ponto de Referência

    obj_media = { 'sala' :  {'vetor_amostras' : [] , 'vetor_auxiliar' : []} , 'quarto' : {'vetor_amostras' : [], 'vetor_auxiliar' : []}, 'cozinha' : {'vetor_amostras' : [], 'vetor_auxiliar' : []}}

    matrizT = [] # Matriz de treinamento que será formada ao longo da execução do algoritmo

    for data_frame_pr in array_dataframes: ## são coletadas as amostras 

        tuplas_leitura_sinal = data_frame_pr.itertuples()

        tuplas_aux = data_frame_pr.itertuples()
        lista_aux = list(tuplas_aux)
        segundo_atual = (datetime.strptime(lista_aux[0].date_time, "%Y-%m-%d %H:%M:%S.%f")).second # pega os segundos da primeira data do dataframe


        for key in obj_media:
            obj_media[key]['vetor_auxiliar'].clear()

        numero_amostras = 0 # tive de inserir um limite de amostras, pois alguns Pontos de Referência tinham menos sinais coletados do que outros

        for leitura_sinal in tuplas_leitura_sinal:

            obj_media[leitura_sinal.device_id]['vetor_auxiliar'].append(leitura_sinal.device_signal) # os valores da intensidade de sinal vão sendo armazenados enquanto não se passa 1 segundo

            novo_segundo = (datetime.strptime(leitura_sinal.date_time, "%Y-%m-%d %H:%M:%S.%f")).second

            if(novo_segundo > segundo_atual): # se passar um segundo, a média dos sinais acumuladas é calulada e  guardada no array de amostras

                vetorBi = []
                
                for key in obj_media:
                    if(len(obj_media[key]['vetor_auxiliar']) == 0):
                        vetorBi.append(0)
                    else:
                        vetorBi.append(int( sum(obj_media[key]['vetor_auxiliar']) / len(obj_media[key]['vetor_auxiliar'])) ) # faz a média dos sinais otidos no intervalo de 1 segundo no Ponto de Referência ( depois trocar pelo cálculo dos quartis)

                    obj_media[key]['vetor_auxiliar'].clear()

                    
                matrizT.append({'ponto_referencia': leitura_sinal.id_addr, 'sinal_cozinha' : vetorBi[0], 'sinal_sala': vetorBi[1] , 'sinal_quarto': vetorBi[2]  }) # armazena a amostra na matriz de treinamento 

                segundo_atual = novo_segundo
                numero_amostras +=1

            if(numero_amostras == 7):
                break
            
   

    dataFrameTreinamento =  pd.DataFrame.from_dict(matrizT) # Cria um novo dataFrame com os valores da Matriz de Treinamento
    print('                      Dataframe de Treinamento: \n\n\n', dataFrameTreinamento)

    # gera um arquivo csv com os dados da matriz de treinamento
    dataFrameTreinamento.to_csv('treinamento_leituras_sinal.csv')

    return dataFrameTreinamento

def executar_knn(dataFrameT):

    X_train, X_test, y_train, y_test = train_test_split(dataFrameT.drop(['ponto_referencia'], 1), dataFrameT['ponto_referencia'], test_size=0.3) 

    print ('\n       Conjunto de Treinamento:   \n\n', X_train)

    print ('\n       Conjunto de Teste:   \n\n', X_test)


    knn = KNeighborsClassifier(n_neighbors=3) 

    print(knn.fit(X_train, y_train))

    resultado = knn.predict(X_test)

    print ('\n              Resultado do KNN: \n\n', pd.crosstab(y_test,resultado, rownames=['Real'], colnames=['Predito'], margins=True))



def main():

    dataFrame = abrir_arquivo()
    dataFrameTreinamento =  montar_matriz_amostras(dataFrame)
    executar_knn(dataFrameTreinamento)


main()