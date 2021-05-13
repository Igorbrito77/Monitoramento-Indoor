# Monitoramento-Indoor

Implementação de um programa que gera pacotes com endereço MAC forjado para a captção de sinais dos Pontos de Acesso de um ambiente fechado visando facilitar a fase de treinamento seguinte.


## Execução 

* Mudar para root para a execução dos seguintes comandos. (**"sudo su"** no terminal do linux)
* Alterar o valor das varáveis no arquivo **script.py** de acordo com as configurações da sua rede wireless.

### Deixar a placa em modo monitor: 

* Verifica quais processos precisam ser interrompidos: **airmon-ng check**
* Encerra os processos:  **airmon-ng check kill**
* Deixa a placa wireless em modo monitor: **airmon-ng start nome_da_placa_wireless**
* Religar o wifi caso tenha sido desligado ao ativar o modo monitor:  **/etc/init.d/network-manager restart**
* Encerrar o modo monitor na placa wireless : **airmon-ng stop nome_da_placa_wireless_em_modo_monitor**

### Execução da geração de pacotes

* Executar o arquivo script_coleta.py : **python script_coleta.py**

### Execução da geração de pacotes com interface gráfica

* Executar o arquivo script.py : **python interface.py**


## Teste da geração de pacotes

* Executar o arquivo pacotes_beacon.py : **python pacotes_beacon.py**
