from scapy.all import Dot11,Dot11Beacon,Dot11Elt,RadioTap,sendp,hexdump

netSSID = 'testSSID' #Network name here
iface = 'wlan0mon'   #Interface name here

dot11 = Dot11(type=0, subtype=8, addr1='ff:ff:ff:ff:ff:ff', addr2='22:22:22:22:22:22', addr3='33:33:33:33:33:33')

## addr1 = MAC de destino
## addr2 = Endereço MAC de origem do remetente.
## addr3 endereço MAC do ponto de acesso.

beacon = Dot11Beacon(cap='ESS+privacy') ## indica a capacidade do ponto de acesso

essid = Dot11Elt(ID='SSID',info=netSSID, len=len(netSSID))

## Para definir a rede como WPA2, precisamos adicionar um Elemento de Informação (IE) de Rede Segura Robusta (RSN) ao nosso quadro de gerenciamento. 
## A variável "rsn" contém essas informações e é especificada para Scapy em hexadecimal.

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
print("\nHexDump of frame")
hexdump(frame)
input("\nPress enter to start\n")

sendp(frame, iface=iface, inter=0.100, loop=1)