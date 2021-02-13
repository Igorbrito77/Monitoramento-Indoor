from Tkinter import *
from scapy.all import Dot11,Dot11Beacon,Dot11Elt,RadioTap,sendp,hexdump
import zlib

class Application:
	def __init__(self, master=None):

		self.fontePadrao = ("Arial", "10")
		self.primeiroContainer = Frame(master)
		self.primeiroContainer["pady"] = 10
		self.primeiroContainer.pack()

		self.segundoContainer = Frame(master)
		self.segundoContainer["padx"] = 20
		self.segundoContainer.pack()

		self.terceiroContainer = Frame(master)
		self.terceiroContainer["padx"] = 20
		self.terceiroContainer.pack()

		self.quartoContainer = Frame(master)
		self.quartoContainer["pady"] = 20
		self.quartoContainer.pack()

		self.quintoContainer = Frame(master)
		self.quintoContainer["pady"] = 20
		self.quintoContainer.pack()
 
		############################################################# TITULO

		self.titulo = Label(self.primeiroContainer, text="Monitoramento Indoor")
		self.titulo["font"] = ("Arial", "10", "bold")
		self.titulo.pack()


		########################################  PONTO DE REFERENCIA:


		self.ponto_referencia_label = Label(self.segundoContainer,text="Nome do Ponto de Referencia", font=self.fontePadrao)
		self.ponto_referencia_label.pack(side=LEFT)

		self.ponto_referencia = Entry(self.segundoContainer)
		self.ponto_referencia["width"] = 30
		self.ponto_referencia["font"] = self.fontePadrao
		self.ponto_referencia.pack(side=LEFT)



		########################################  NUMERO DE PACOTES:


		self.numero_pacotes_label = Label(self.terceiroContainer,text="Numero de pacotes", font=self.fontePadrao)
		self.numero_pacotes_label.pack(side=LEFT)

		self.numero_pacotes = Entry(self.terceiroContainer)
		self.numero_pacotes["width"] = 30
		self.numero_pacotes["font"] = self.fontePadrao
		self.numero_pacotes.pack(side=LEFT)


		########################################  INETERVALO DE ENVIO:


		self.intervalo_label = Label(self.terceiroContainer, text="Intervalo de envio", font=self.fontePadrao)
		self.intervalo_label.pack(side=LEFT)

		self.intervalo = Entry(self.terceiroContainer)
		self.intervalo["width"] = 30
		self.intervalo["font"] = self.fontePadrao
		self.intervalo.pack(side=LEFT)


		########################################  BOTAO DE INICIO:

		self.botao_inicio = Button(self.quartoContainer)
		self.botao_inicio["text"] = "Iniciar"
		self.botao_inicio["font"] = ("Calibri", "8")
		self.botao_inicio["width"] = 12
		self.botao_inicio["command"] = self.enviar_pacotes
		self.botao_inicio.pack()


		########################################  BOTAO DE PARAR:


		# self.autenticar = Button(self.quintoContainer)
		# self.autenticar["text"] = "nao ta pronto kkkk"
		# self.autenticar["font"] = ("Calibri", "8")
		# self.autenticar["width"] = 12
		# self.autenticar["command"] = self.verificaSenha
		# self.autenticar.pack()



		########################################  MENSAGEM DE EXCECAO:

		self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
		self.mensagem.pack()

	#Metodo verificar senha
	# def verificaSenha(self):
	# 	usuario = self.numero_pacotes.get()
	# 	senha = self.senha.get()
	# 	if usuario == "usuariodevmedia" and senha == "dev":
	# 		self.mensagem["text"] = "Autenticado"
	# 	else:
	# 		self.mensagem["text"] = "Erro na autenticacao"

	def enviar_pacotes(self):

		ponto_referencia = self.ponto_referencia.get()
		numero_pacotes = 	self.numero_pacotes.get()
		intervalo_envio = self.intervalo.get()

		if ponto_referencia == "":
			self.mensagem["text"] = "Insira o nome do Ponto de Referencia"
			return

		if numero_pacotes == "":
			self.mensagem["text"] = "Insira o numero de pacotes"
			return

		if intervalo_envio == "":
			self.mensagem["text"] = "Insira o interevalo de envio"
			return

		self.geracao_pacotes()

	def criacao_mac_ponto_referencia(self):

		ponto_referencia = self.ponto_referencia.get()

		print(ponto_referencia)

		prefixo = '0000'
		sufixo = hex( zlib.crc32(ponto_referencia) % (1<<32))

		hash_nome_pr = prefixo + sufixo.replace('0x', '')

		mac_forjado = ':'.join(s.encode('hex') for s in hash_nome_pr.decode('hex'))


		print '\n____________________________________________________\n'
		print 'Sufixo: '+  sufixo
		print '\nEndereco MAC forjado: ' + mac_forjado
		print '\n____________________________________________________\n'
		

		return mac_forjado

	def geracao_pacotes(self):

		netSSID = 'testSSID' 
		iface = 'wlp3s0mon'   #Nome da Interface Wireless

		mac_forjado_pr = self.criacao_mac_ponto_referencia()
		numero_pacotes = int(self.numero_pacotes.get())
		intervalo_envio = float(self.intervalo.get())

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

		# print '\n\n____________________________________________________\n'
		# raw_input("Digite enter para o inicio do envio de pacotes:")


		a = sendp(frame, iface=iface, inter=intervalo_envio, loop=0, count=numero_pacotes) # inter = intervalo entre o envio dos pacotes
		print(a)

		self.primeiroContainer.quit()




root = Tk()
Application(root)
root.mainloop()