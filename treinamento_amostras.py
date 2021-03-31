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

        # segundos do intervalo, numero de amostras, 
    
    numero_amostras = int(input('Insira o número de amostras que serão geradas para cada Ponto de Referência: '))
    segundos_intervalo = int(input('Insira o número de segundos para a montagem de uma amostra para um Ponto de Referência: '))

    ## separa o dataframe em partes, sendo que cada parte corresponde às leituras de sinal correspondentes a um Ponto de Referência específico
    dt_PR_1 =  (dataFrame[ (dataFrame['id_addr']  == 131341)]) # quarto2
    dt_PR_2 =  (dataFrame[ (dataFrame['id_addr']  == 131364)]) # cozinha
    dt_PR_3 =  (dataFrame[ (dataFrame['id_addr']  == 131402)]) # quarto3
    dt_PR_4 =  (dataFrame[ (dataFrame['id_addr']  == 131428)]) # sala
    dt_PR_5 =  (dataFrame[ (dataFrame['id_addr']  == 131451)]) # banheiro
    dt_PR_6 =  (dataFrame[ (dataFrame['id_addr']  == 131482)]) # quarto1
    dt_PR_7 =  (dataFrame[ (dataFrame['id_addr']  == 131717)]) # corredor

    nomes_pr = {  131341 : 'quarto2', 131364 : 'cozinha', 131402 : 'quarto3', 131428 : 'sala', 131451 : 'banheiro', 131482 : 'quarto1', 131717 : 'corredor' }


    array_dataframes = [dt_PR_1, dt_PR_2, dt_PR_3, dt_PR_4, dt_PR_5, dt_PR_6, dt_PR_7] # cria um array contendo os dataframes de cada Ponto de Referência

    obj_media = { 'sala' :  {'vetor_amostras' : [] , 'vetor_auxiliar' : []} , 'quarto' : {'vetor_amostras' : [], 'vetor_auxiliar' : []}, 'cozinha' : {'vetor_amostras' : [], 'vetor_auxiliar' : []}}

    matrizT = [] # Matriz de treinamento que será formada ao longo da execução do algoritmo

    for data_frame_pr in array_dataframes: ## são coletadas as amostras 

        tuplas_leitura_sinal = data_frame_pr.itertuples()

        tuplas_aux = data_frame_pr.itertuples()
        lista_aux = list(tuplas_aux)
        data_atual = datetime.strptime(lista_aux[0].date_time, "%Y-%m-%d %H:%M:%S.%f") # pega a primeira data do dataframe


        for key in obj_media:
            obj_media[key]['vetor_auxiliar'].clear()

        cont_amostras = 0 # tive de inserir um limite de amostras, pois alguns Pontos de Referência tinham menos sinais coletados do que outros

        for leitura_sinal in tuplas_leitura_sinal:

            obj_media[leitura_sinal.device_id]['vetor_auxiliar'].append(leitura_sinal.device_signal) # os valores da intensidade de sinal vão sendo armazenados enquanto não se passa 1 segundo

            nova_data = datetime.strptime(leitura_sinal.date_time, "%Y-%m-%d %H:%M:%S.%f")

            if((nova_data - data_atual) >= timedelta(seconds=segundos_intervalo)): # se passar X segundos, a média dos sinais acumuladas é calulada e  guardada no array de amostras

                vetorBi = []
                
                for key in obj_media:
                    if(len(obj_media[key]['vetor_auxiliar']) == 0): #### tartar esse 0 - definir como -98 (ruído de fundo )
                        vetorBi.append(-98)
                    else:
                        vetorBi.append(int( sum(obj_media[key]['vetor_auxiliar']) / len(obj_media[key]['vetor_auxiliar'])) ) # faz a média dos sinais otidos no intervalo de 1 segundo no Ponto de Referência ( depois trocar pelo cálculo dos quartis)

                    obj_media[key]['vetor_auxiliar'].clear()

                    
                matrizT.append({'ponto_referencia':  nomes_pr[leitura_sinal.id_addr], 'sinal_cozinha' : vetorBi[0], 'sinal_sala': vetorBi[1] , 'sinal_quarto': vetorBi[2]  }) # armazena a amostra na matriz de treinamento 

                data_atual = nova_data
                cont_amostras +=1

            if(cont_amostras == numero_amostras ):
                break
            
    dataFrameTreinamento =  pd.DataFrame.from_dict(matrizT) # Cria um novo dataFrame com os valores da Matriz de Treinamento
    print('                                                             DATAFRAME DE TREINAMENTO: \n\n\n', dataFrameTreinamento)

    # gera um arquivo csv com os dados da matriz de treinamento
    dataFrameTreinamento.to_csv('treinamento_leituras_sinal.csv')

    return dataFrameTreinamento

def executar_knn(dataFrameT):

    # aleatoriedade (boolean), partição de testes
    porcentagem_testes = float(input('Insira a porcentagem de partição de amostras para Teste (exemplo: 0.5 = 50%) : '))
    
    aleatoriedade = input('Utilizar aleatoriedade na partição das amostras de testes e treinamento ? (Sim = S, Não = N)  : ')

    aleatoriedade = 42 if aleatoriedade == 'S' else None

    X_train, X_test, y_train, y_test = train_test_split(dataFrameT.drop(['ponto_referencia'], 1), dataFrameT['ponto_referencia'],test_size=porcentagem_testes, stratify= dataFrameT['ponto_referencia'], random_state=aleatoriedade) 


    knn = KNeighborsClassifier(n_neighbors=3)

    print(knn.fit(X_train, y_train))

    resultado = knn.predict(X_test)
    
    conjunto_teste = pd.DataFrame(X_test)
    conjunto_teste['ponto_referencia'] = y_test 
    print ('\n____________________________________________________________________________________________________________________________')
    print ('\n                                                          CONJUNTO DE TESTE   \n\n', conjunto_teste)

    conjunto_teste['predicao_knn'] =  resultado

    tuplas = conjunto_teste.itertuples()

    acertos =[] 
    for tupla in tuplas:
        if tupla.ponto_referencia == tupla.predicao_knn:
            acertos.append('V')        
        else:
            acertos.append('X')

    conjunto_teste['acerto'] =  acertos

    print ('\n____________________________________________________________________________________________________________________________')
    print('\n                                                       PREDIÇÃO DO KNN NO CONJUNTO DE TESTE \n\n', conjunto_teste)

    print ('\n____________________________________________________________________________________________________________________________')
    print ('\n                                                      RESULTADO GERAL DO KNN \n\n', pd.crosstab(y_test,resultado, rownames=['Real'], colnames=['Predito'], margins=True))

    target_names = sorted(y_test.unique())

    print ('\n____________________________________________________________________________________________________________________________')
    print('\n                                                       MÉTRICAS DE COMPARAÇÃO \n\n', metrics.classification_report(y_test,resultado,target_names= target_names, zero_division = 0))


    # cria um dataframe com o report das métricas de classificação

    dicionario_report =  metrics.classification_report(y_test,resultado,target_names= target_names, zero_division = 0,  output_dict=True)
    dataFrameReport = pd.DataFrame(dicionario_report).transpose()
    dataFrameReport.to_csv('report_amostras.csv')



## segundos do intervalo, numero de amostras, aleatoriedade (boolean), partição de testes, nome do arquivo csv gerado


def main():

    dataFrame = abrir_arquivo()
    dataFrameTreinamento =  montar_matriz_amostras(dataFrame)
    executar_knn(dataFrameTreinamento)


main()


## tratar o  0 no ponto de sinal, leavndo em conta o ruído (-98 ou -95)                                                                                                         X
## separar o dataframe (separaa antes de montar a matriz) pra ter as partes de treinamento e teste                                                                              +-
## alterar o split no dataset de treinamento e teste ( ter o mesmo número de amostras de testes opara cada PR)                                                                  X
###  calcular a taxa de erro / acerto  por Ponto de referencia após a execução do knn                                                                                           X
### ao invés de usar o critério de  maioria, talvez usar média ponderada ou outra medida ......  )  


