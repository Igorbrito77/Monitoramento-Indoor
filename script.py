from scapy.all import Dot11,Dot11Beacon,Dot11Elt,RadioTap,sendp,hexdump
# import hashlib


def geracao_pacotes():

	netSSID = 'testSSID' 
	iface = 'wlp3s0mon'   #Nome da Interface Wireless


	## addr1 = MAC de destino (MAC da placa wireless)
	## addr2 = Endereco MAC de origem do remetente. (MAC forjado)
	## addr3 = Endereco MAC do ponto de acesso.

	# dot11 = Dot11(type=0, subtype=8, addr1='E4:18:6B:4B:94:00', addr2=nome_pr_criptografado, addr3='33:33:33:33:33:33')
	dot11 = Dot11(type=0, subtype=8, addr1='E4:18:6B:4B:94:00', addr2='22:22:22:22:22:22', addr3='33:33:33:33:33:33')


	beacon = Dot11Beacon(cap='ESS+privacy') ## indica a capacidade do ponto de acesso

	essid = Dot11Elt(ID='SSID',info=netSSID, len=len(netSSID))


	rsn = Dot11Elt(ID='RSNinfo', info=(
	'\x01\x00'
	'\x00\x0f\xac\x02'
	'\x02\x00'
	'\x00\x0f\xac\x04'
	'\x00\x0f\xac\x02'
	'\x01\x00'
	'\x00\x0f\xac\x02'
	'\x00\x00'))

	frame = RadioTap()/dot11/beacon/essid/rsn

	frame.show()
	print("HexDump of frame")

	hexdump(frame)

	raw_input("Digite enter para o inicio do envio de pacotes:")

	sendp(frame, iface=iface, inter=0.100, loop=1) # inter = intervalo entre o envio dos pacotes



def criptografa_nome_pr():

	# nome_pr = raw_input('Digite o nome do Ponto de Referencia: ')

	# h = hashlib.md5()
	# h.update(nome_pr)
	# nome_pr_hex = h.hexdigest()
	# print(nome_pr_hex)

	pass


def main():
	# nome_pr_criptografado = criptografa_nome_pr()
	# geracao_pacotes(nome_pr_criptografado)

	geracao_pacotes()



main()