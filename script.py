from scapy.all import Dot11,Dot11Elt,RadioTap,sendp
import binascii 
from math import ceil 
from hashlib import sha256 


def geracao_pacotes():

	nome_ponto_referencia = input('Insira o nome do Ponto de Referência: ')
	mac_forjado_pr = criacao_mac_ponto_referencia(nome_ponto_referencia)
	print(mac_forjado_pr)

	tempo_execucao = float(input("Insira o tempo de execucao (minutos): "))
	intervalo_envio = float(input("Insira o intervalo de frequencia de envio de pacotes (em segundos) : "))
	num_pacotes = (tempo_execucao * 60)/intervalo_envio


	data = "UFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJUFRRJ"

	## addr1 = MAC de destino (MAC da placa wireless)
	## addr2 = Endereco MAC de origem do remetente. (MAC forjado)
	## addr3 = Endereco MAC do ponto de acesso.
	dot11 = Dot11(type=2, subtype=0, addr1='E4:18:6B:4B:94:00', addr2=mac_forjado_pr, addr3='33:33:33:33:33:33')

	essid = Dot11Elt(ID='SSID',info='testSSID', len=len('testSSID')) # indica a capacidade do ponto de acesso

	frame = RadioTap()/dot11/essid/data

	frame.show()
	 
	input("Digite enter para o inicio do envio de pacotes:")


	sendp(frame, iface='wlp3s0mon', inter=intervalo_envio, loop=0, count=num_pacotes) # iface = Nome da Interface Wireless. inter = intervalo entre o envio dos pacotes (em segundos). count = numero de pacotes 

	escreve_arquivo(nome_ponto_referencia, mac_forjado_pr)


def criacao_mac_ponto_referencia(nome_ponto_referencia):

	numero_bits_sufixo = 24

	result = [] 

	# Produz resumos de SHA512 suficientes para fazer um resumo composto maior ou igual a N bits
	for i in range(ceil(numero_bits_sufixo / 256)): 

		# Anexa contagem de iteração à mensagem
		currentMsg = str(nome_ponto_referencia) + str(i) 

		# Adiciona hash atual à lista de resultados
		result.append(sha256((currentMsg).encode()).hexdigest())

	# Anexa todos os hashes computados
	result = ''.join(result) 
	
	# Obtenção de representação binária
	resAsBinary = ''.join(format(ord(x), 'b') for x in result) 
	
	# Cortando o hash para o tamanho necessário pegando apenas os bits iniciais 
	resAsBinary = resAsBinary[:numero_bits_sufixo] 
			
	# Converte de volta para o formato ASCII binário
	sufixo = binascii.unhexlify('00%x' % int(resAsBinary, 2)).hex() 
	
	hash_nome_pr = '000000' + sufixo.replace('00', '')

	array_mac = []
	for i in range(0, 12, 2):
		array_mac.append(hash_nome_pr[i] + hash_nome_pr[i+1])

	return ':'.join(array_mac)	

def escreve_arquivo(nome_ponto_referencia, mac_forjado_pr):

	with open('lista_ponto_referencias.txt', 'a') as arquivo:
		arquivo.write('\n ' + nome_ponto_referencia+ ' | '+ mac_forjado_pr)
	arquivo.close()


def main():
	geracao_pacotes()


main()