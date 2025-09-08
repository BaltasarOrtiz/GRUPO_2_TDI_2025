# Tabla de caracteres que se pueden comprimir, cada uno representado por 3 bits
# Tabla de caracteres que se pueden comprimir, cada uno representado por 3 bits (2^3 = 8 caracteres)
__table = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] # 3 bits por caracter

def __bytes_to_binary_string(string):
	"""
	Convierte una secuencia de bytes en una cadena binaria.
	
	:param string: Secuencia de bytes a convertir.
	:return: Cadena binaria que representa la secuencia de bytes.
	"""
	# Convierte cada byte a su representación binaria de 8 bits y los concatena
	return ''.join(format(i, '08b') for i in string)

def compress(str):
	"""
	Comprime una cadena utilizando una tabla de caracteres predefinida.
	Cada caracter se codifica con 3 bits en lugar de 8 bits (ASCII).
	
	:param str: Cadena a comprimir (solo debe contener caracteres de la tabla).
	:return: Buffer binario comprimido en forma de bytearray.
	"""
	s = ''
	# Convierte cada carácter de la cadena en su representación binaria de 3 bits
	# utilizando el índice del caracter en la tabla
	for c in str:
		s += format(__table.index(c), '03b')
	
	# Calcula cuántos bits de padding necesitamos para completar el último byte
	# Se añaden 3 bits al inicio para almacenar el número de bits de padding
	remainder = 8 - (len(s) + 3) % 8
	
	# Añade el número de bits de relleno al inicio (3 bits para indicar el padding)
	s = format(remainder, '03b') + s
	
	# Añade los bits de relleno (ceros) al final para completar bytes completos
	s += '0' * remainder
	
	# Convierte la cadena binaria en un bytearray, procesando grupos de 8 bits
	bytes = bytearray([int(s[i : i + 8], 2) for i in range(0, len(s), 8)])
	
	# print(f'Compressed: {str} => {s} => {bytes}')
	return bytes
	
def decompress(bytes):
	"""
	Descomprime un buffer binario en una cadena utilizando una tabla de caracteres predefinida.
	
	:param bytes: Buffer binario comprimido en forma de bytearray.
	:return: Cadena descomprimida.
	"""
	# Convierte el bytearray comprimido de vuelta a una cadena binaria
	s = __bytes_to_binary_string(bytes)
	
	# Lee los primeros 3 bits para obtener el número de bits de padding
	remainder = int(s[:3], 2)
	
	str = ''
	# Procesa la cadena binaria en grupos de 3 bits, excluyendo:
	# - Los primeros 3 bits (información de padding)
	# - Los últimos 'remainder' bits (padding)
	for i in range(3, len(s) - remainder, 3):
		# Convierte cada grupo de 3 bits a índice y busca el caracter en la tabla
		str += __table[int(s[i : i+3], 2)]
	
	# print(f'Decompressed: {bytes} => {s} => {str}')
	return str

if __name__ == '__main__':
	import random
	
	# Genera una cadena de prueba aleatoria utilizando los caracteres de la tabla
	test_str = ''.join([random.choice(__table) for _ in range(5)])
	
	# Proceso de compresión
	compressed = compress(test_str)
	
	# Proceso de descompresión
	decompressed = decompress(compressed)

	# Muestra los resultados del proceso de compresión/descompresión
	print('Original:', test_str)
	print('Compressed size:', len(test_str) * 3 / 8, 'bytes')  # Tamaño teórico
	print('Compressed:', compressed)
	compressed_binary = __bytes_to_binary_string(compressed)
	print(f'Compressed (binary): {compressed_binary} ({len(compressed_binary)} bits)')
	print('Decompressed:', decompressed)

	# Verifica la integridad del proceso: la cadena descomprimida debe ser igual a la original
	assert test_str == decompressed, 'Error: decompressed string is not equal to original string'