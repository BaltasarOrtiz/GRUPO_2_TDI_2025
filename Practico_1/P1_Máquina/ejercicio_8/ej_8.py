# 8. Implementar un programa que valide un CUIT/CUIL ingresado por teclado.

# Constantes para la validación
base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]  # Multiplicadores para cada posición del CUIT/CUIL
tipos_cuil = [20, 23, 24, 27]  # Tipos válidos para CUIL (personas físicas)
tipos_cuit = [30, 33, 34]      # Tipos válidos para CUIT (personas jurídicas)
tipos = tipos_cuil + tipos_cuit # Todos los tipos válidos

def tipo2(tipo):
	"""
	Determina si un tipo corresponde a CUIL o CUIT.
	
	Args:
		tipo (int): Los primeros dos dígitos del CUIT/CUIL
		
	Returns:
		str: "CUIL" o "CUIT"
		
	Raises:
		ValueError: Si el tipo no es válido
	"""
	if tipo in tipos_cuil: 
		return "CUIL"
	if tipo in tipos_cuit: 
		return "CUIT"
	raise ValueError("Tipo de CUIL/CUIT no valido")

def validar_cuit(cuit):
	"""
	Valida un CUIT/CUIL según el algoritmo oficial.
	
	Args:
		cuit (str): CUIT/CUIL en formato XX-XXXXXXXX-X
		
	Returns:
		tuple: (bool, str) - (es_válido, tipo)
	"""
	# Elimina espacios en blanco al inicio y al final
	cuit = cuit.strip()
 
	# Verifica el formato del CUIT/CUIL (XX-XXXXXXXX-X)
	if len(cuit) != 13 or cuit[2] != "-" or cuit[11] != "-":
		return False, "CUIT/CUIL"

	# Obtiene el tipo (los primeros dos dígitos)
	tipo = int(cuit[:2])
	if tipo not in tipos: 
		return False, "CUIT/CUIL"
 
	# Convierte solo los dígitos a una lista de enteros (elimina guiones)
	cuit_digitos = [int(i) for i in cuit if i.isdigit()]
 
	# Calcula la suma ponderada de los primeros 10 dígitos
	suma_ponderada = sum(
		cuit_digitos[i] * base[i] for i in range(10)
	)
 
	# Calcula el dígito verificador esperado
	resto = suma_ponderada % 11
	digito_verificador = 11 - resto

	# Casos especiales para el dígito verificador
	if digito_verificador == 11: 
		digito_verificador = 0
	if digito_verificador == 10: 
		digito_verificador = 9
	
	# Verifica si el dígito verificador calculado coincide con el ingresado
	# y retorna el resultado junto con el tipo
	es_valido = digito_verificador == cuit_digitos[10]
	return es_valido, tipo2(tipo)


# Ejemplos de uso (descomentados para pruebas)
# print(validar_cuit("20-12345678-9"))  # (False, 'CUIL')
# print(validar_cuit("20-43926518-4"))  # (True, 'CUIL')

if __name__ == "__main__":
	# Programa principal: solicita CUIT/CUIL al usuario y lo valida
	cuit = input("Ingrese un CUIT/CUIL (con guiones): ")
	es_valido, tipo = validar_cuit(cuit)
	
	if es_valido:
		print(f"El {tipo} ingresado es válido")
	else:
		print(f"El {tipo} ingresado no es válido")