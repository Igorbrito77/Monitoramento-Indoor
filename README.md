# Monitoramento-Indoor

Implementação de um programa que gera pacotes com endereço MAC forjado para a captção de sinais dos Pontos de Acesso de um ambiente fechado visando facilitar a fase de treinamento seguinte.


## Execução 

### Deixar a placa em modo monitor: 
---

* Verifica quais processos precisam ser interrompidos: **airmon-ng check**
* Encerra os processos:  **airmon-ng check kill**
* Deixa a placa wireless em modo monitor: **airmon-ng start nome_da_placa_wireless**
* Religar o wifi caso tenha sido desligado ao ativar o modo monitor:  **/etc/init.d/network-manager restart**
* Encerrar o modo monitor na placa wireless : **airmon-ng stop nome_da_placa_wireless**


* Executar o arquivo script.py : **python script.py**


## Teste da geração de pacotes
------

* Executar o arquivo pacotes_beacon.py : **python pacotes_beacon.py**
