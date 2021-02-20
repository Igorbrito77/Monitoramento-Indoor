# Python program to demonstrate 
# repeated hashing with 
# concatenation 

import binascii 
from math import ceil 
from hashlib import sha256 

# Function to perform Full Domain 
# Hash of 'message' using 
# SHA512 with a digest of 
# N bits 
def fdh(message, n): 
	

	result = [] 

	# Produz resumos de SHA512 suficientes para fazer um resumo composto maior ou igual a N bits
	for i in range(ceil(n / 256)): 

		# Anexa contagem de iteração à mensagem
		currentMsg = str(message) + str(i) 

		# Adicionar hash atual à lista de resultados
		result.append(sha256((currentMsg).encode()).hexdigest())

	# Anexar todos os hashes computados
	result = ''.join(result) 
	
	print(result)

	# Obtenção de representação binária
	resAsBinary = ''.join(format(ord(x), 'b') for x in result) 
	
	# Cortando o hash para o tamanho necessário pegando apenas os bits iniciais 
	resAsBinary = resAsBinary[:n] 
		
	print('Binário cortado --->', resAsBinary)
	
	# Converter de volta para o formato ASCII binário
	sufixo = binascii.unhexlify('00%x' % int(resAsBinary, 2)).hex() 
	
	hash_nome_pr = '000000' + sufixo.replace('00', '')

	array_mac = []
	for i in range(0, 12, 2):
		array_mac.append(hash_nome_pr[i] + hash_nome_pr[i+1])

	return ':'.join(array_mac)	



# Driver code 
if __name__ == '__main__': 
	# Message to be hashed 
	message = input('Insira o nome do Ponto de Referência:')

	# Generate a 600 bit hash using SHA256 
	print(fdh(message, 24)) 

