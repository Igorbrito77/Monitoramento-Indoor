# Monitoramento-Indoor

Implementação de um programa que gera pacotes com endereço MAC forjado para a captção de sinais dos Pontos de Acesso de um ambiente fechado visando facilitar a fase de treinamento seguinte.


Execução 
----

Deixar a placa em modo monitor: 
---

* airmon-ng check
* airmon-ng check kill
* airmon-ng start wlp3s0
* /etc/init.d/network-manager restart
* airmon-ng stop wlp3s0mon


* Executar o arquivo script.py : python script.py


Teste da geração de pacotes
------

* Executar o arquivo pacotes_beacon.py : python pacotes_beacon.py
