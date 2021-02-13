from tkinter import *

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


		self.autenticar = Button(self.quintoContainer)
		self.autenticar["text"] = "nao ta pronto kkkk"
		self.autenticar["font"] = ("Calibri", "8")
		self.autenticar["width"] = 12
		self.autenticar["command"] = self.verificaSenha
		self.autenticar.pack()

		self.mensagem = Label(self.quartoContainer, text="", font=self.fontePadrao)
		self.mensagem.pack()

	#Metodo verificar senha
	def verificaSenha(self):
		usuario = self.numero_pacotes.get()
		senha = self.senha.get()
		if usuario == "usuariodevmedia" and senha == "dev":
			self.mensagem["text"] = "Autenticado"
		else:
			self.mensagem["text"] = "Erro na autenticação"

	def enviar_pacotes(self):
		
		ponto_referencia = self.ponto_referencia.get()
		numero_pacotes = self.numero_pacotes.get()
		intervalo = self.intervalo.get()


		print(ponto_referencia)
		print(numero_pacotes)
		print(intervalo)
	



root = Tk()
Application(root)
root.mainloop()