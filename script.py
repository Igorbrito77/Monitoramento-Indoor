# from scapy.all import Dot11,Dot11Beacon,Dot11Elt,RadioTap,sendp,hexdump
# import zlib
import binascii 
from math import ceil 
from hashlib import sha256 


def geracao_pacotes():

	nome_ponto_referencia = input('Insira o nome do Ponto de Referência: ')
	mac_forjado_pr = criacao_mac_ponto_referencia(nome_ponto_referencia)
	print(mac_forjado_pr)

	with open('lista_ponto_referencias.txt', 'a') as arquivo:
		arquivo.write('\n ' + nome_ponto_referencia+ ' . '+ mac_forjado_pr)
	arquivo.close()

	# netSSID = 'testSSID' 
	# iface = 'wlp3s0mon'   #Nome da Interface Wireless


	# tempo_execucao = float(input("Insira o tempo de execucao (minutos): "))
	# intervalo_envio = float(input("Insira o intervalo de frequencia de envio de pacotes (em segundos) : "))
	# num_pacotes = (tempo_execucao * 60)/intervalo_envio

	# ## addr1 = MAC de destino (MAC da placa wireless)
	# ## addr2 = Endereco MAC de origem do remetente. (MAC forjado)
	# ## addr3 = Endereco MAC do ponto de acesso.

	# dot11 = Dot11(type=0, subtype=8, addr1='E4:18:6B:4B:94:00', addr2=mac_forjado_pr, addr3='33:33:33:33:33:33')

	# beacon = Dot11Beacon(cap='ESS+privacy') ## indica a capacidade do ponto de acesso

	# essid = Dot11Elt(ID='SSID',info=netSSID, len=len(netSSID))


	# rsn = Dot11Elt(ID='RSNinfo', info=(
	# '\x01\x00'
	# '\x00\x0f\xac\x02'
	# '\x02\x00'
	# '\x00\x0f\xac\x04'
	# '\x00\x0f\xac\x02'
	# '\x01\x00'
	# '\x00\x0f\xac\x02'
	# '\x00\x00'))

	# frame = RadioTap()/dot11/beacon/essid/rsn

	# frame.show()
	# print("HexDump of frame")

	# hexdump(frame)

	# # print '\n\n____________________________________________________\n'
	# raw_input("Digite enter para o inicio do envio de pacotes:")


	# sendp(frame, iface=iface, inter=intervalo_envio, loop=0, count=num_pacotes) # inter = intervalo entre o envio dos pacotes



def criacao_mac_ponto_referencia(nome_ponto_referencia):

	numero_bits_sufixo = 24

	result = [] 

	# Produz resumos de SHA512 suficientes para fazer um resumo composto maior ou igual a N bits
	for i in range(ceil(numero_bits_sufixo / 256)): 

		# Anexa contagem de iteração à mensagem
		currentMsg = str(nome_ponto_referencia) + str(i) 

		# Adicionar hash atual à lista de resultados
		result.append(sha256((currentMsg).encode()).hexdigest())

	# Anexar todos os hashes computados
	result = ''.join(result) 
	
	# Obtenção de representação binária
	resAsBinary = ''.join(format(ord(x), 'b') for x in result) 
	
	# Cortando o hash para o tamanho necessário pegando apenas os bits iniciais 
	resAsBinary = resAsBinary[:numero_bits_sufixo] 
			
	# Converter de volta para o formato ASCII binário
	sufixo = binascii.unhexlify('00%x' % int(resAsBinary, 2)).hex() 
	
	hash_nome_pr = '000000' + sufixo.replace('00', '')

	array_mac = []
	for i in range(0, 12, 2):
		array_mac.append(hash_nome_pr[i] + hash_nome_pr[i+1])

	return ':'.join(array_mac)	
	

def main():
	# mac_forjado_pr = criacao_mac_ponto_referencia()
	geracao_pacotes()



main()