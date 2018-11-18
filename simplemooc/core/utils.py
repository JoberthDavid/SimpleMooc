import hashlib
import string
import random

def random_key(size=5):
	chars = string.ascii_uppercase + string.digits # atribue à variável chars as letras e números possíveis para fazer a randomização
	return ''.join(random.choice(chars) for x in range(size)) #aplica o método random tendo como opções dentro da variável chars e faz para todos os dígitos por meio de um laço de repetição

def generate_hash_key(salt, random_str_size=5):
	random_str = random_key(random_str_size) #aplica o método random_key e atribue à variável random_str
	text = random_str + salt #cria a variável salt para diminuir a possibilidade de repetição de senha randomica, poderá ser algum dado do usuário
	return hashlib.sha224(text.encode('utf-8')).hexdigest() #aplica os métodos de criptografia do Django