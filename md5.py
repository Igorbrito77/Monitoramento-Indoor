import hashlib 
import binascii 

  
# initializing string 
str2hash = "GeeksforGeeks"
  
# encoding GeeksforGeeks using encode() 
# then sending to md5() 
result = hashlib.md5(str2hash.encode()) 
  
# printing the equivalent hexadecimal value. 
print("The hexadecimal equivalent of hash is : ", end ="") 
print(result.hexdigest()) 

result = result.hexdigest()

resAsBinary = ''.join(format(ord(x), 'b') for x in result) 
# Cortando o hash para o tamanho necessário pegando apenas os bits iniciais 
print(resAsBinary)	

print('len = ', len(resAsBinary))

resAsBinary = resAsBinary[(len(resAsBinary) - 24):len(resAsBinary)] 

print('len = ', len(resAsBinary))
		
print(resAsBinary)	

sufixo = binascii.unhexlify('00%x' % int(resAsBinary, 2)).hex() 

hash_nome_pr = '000000' + sufixo.replace('00', '')

array_mac = []
for i in range(0, 12, 2):
	array_mac.append(hash_nome_pr[i] + hash_nome_pr[i+1])

print(':'.join(array_mac))	
