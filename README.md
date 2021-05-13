# Monitoramento-Indoor

Implementação de um programa responsável por realizar uma coleta automatizada de assinaturas de RSSI. Tal ferramenta será utilizada durante a execução da faseo ffline do Wi-Fifingerprint,criando uma base de dados com instâncias previamente classificadas de RSSI que futuramente será utilizada para efetuar a localização na fase online. Este auxílio na fase offline contribuirá com o processo de criação de sistemas de localização indoor que façam uso de tal técnica, ajudando na popularização dos sistemas de localização indoor.


## Execução 

* Mudar para root para a execução dos seguintes comandos. (**"sudo su"** no terminal do linux)
* Alterar o valor das varáveis no arquivo **script.py** de acordo com as configurações da sua rede wireless.

### Deixar a placa em modo monitor: 

* Verifica quais processos precisam ser interrompidos: **airmon-ng check**
* Encerra os processos:  **airmon-ng check kill**
* Deixa a placa wireless em modo monitor: **airmon-ng start nome_da_placa_wireless**
* Religar o wifi caso tenha sido desligado ao ativar o modo monitor:  **/etc/init.d/network-manager restart**
* Encerrar o modo monitor na placa wireless : **airmon-ng stop nome_da_placa_wireless_em_modo_monitor**

### Execução do script de geração de pacotes para a montagem da base de dados

* Executar o arquivo script_coleta.py : **python script_coleta.py**

### Execução do script de validação da base de dados gerada com o script anterior

* Executar o arquivo script_coleta.py : **python script_validacao.py**

### Execução da geração de pacotes com interface gráfica

* Executar o arquivo interface.py : **python interface.py**


## Teste da geração de pacotes

* Executar o arquivo geracao_pacotes.py : **python geracao_pacotes.py**
