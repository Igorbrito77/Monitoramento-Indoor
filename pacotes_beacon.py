from scapy.all import Dot11,Dot11Beacon,Dot11Elt,RadioTap,sendp,hexdump

netSSID = 'testSSID' #Network name here
iface = 'wlp3s0mon'   #Interface name here

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

raw_input("Press enter to start")

sendp(frame, iface=iface, inter=0.100, loop=1)