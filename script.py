from scapy.all import Dot11,Dot11Beacon,Dot11Elt,RadioTap,sendp,hexdump
import zlib


def geracao_pacotes(mac_forjado_pr):

	netSSID = 'testSSID' 
	iface = 'wlp3s0mon'   #Nome da Interface Wireless


	## addr1 = MAC de destino (MAC da placa wireless)
	## addr2 = Endereco MAC de origem do remetente. (MAC forjado)
	## addr3 = Endereco MAC do ponto de acesso.

	dot11 = Dot11(type=0, subtype=8, addr1='E4:18:6B:4B:94:00', addr2=mac_forjado_pr, addr3='33:33:33:33:33:33')

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

	print '\n\n____________________________________________________\n'
	raw_input("Digite enter para o inicio do envio de pacotes:")

	sendp(frame, iface=iface, inter=0.100, loop=1) # inter = intervalo entre o envio dos pacotes



def criacao_mac_ponto_referencia():

	prefixo = '0000'

	nome_pr = raw_input('Digite o nome do Ponto de Referencia: ')

	sufixo = hex( zlib.crc32(nome_pr) % (1<<32))


	hash_nome_pr = prefixo + sufixo.replace('0x', '')

	mac_forjado = ':'.join(s.encode('hex') for s in hash_nome_pr.decode('hex'))


	print '\n____________________________________________________\n'
	print 'Sufixo: '+  sufixo
	print '\nEndereco MAC forjado: ' + mac_forjado
	print '\n____________________________________________________\n'
	

	return mac_forjado


def main():
	mac_forjado_pr = criacao_mac_ponto_referencia()
	geracao_pacotes(mac_forjado_pr)



main()