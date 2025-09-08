import math
import os
import time
from collections import Counter

"""
3. Desarrollar una aplicación de software que calcule la entropía y redundancia, de una fuente con símbolos vistos
en forma independiente y dependiente en O(1). Realizar comparaciones para diferentes archivos (*.txt, *.exe,
*.zip etc.)
"""
def calcular_probabilidades(data):
	"""
	Calcula las probabilidades de cada símbolo en los datos.
	
	Args:
		data: Secuencia de datos (bytes o caracteres)
		
	Returns:
		dict: Diccionario con símbolos como claves y sus probabilidades como valores
	"""
	total = len(data)
	frecuencias = Counter(data)
	return {char: freq / total for char, freq in frecuencias.items()}

def entropia_independiente(data):
	"""
	Calcula la entropía de Shannon para símbolos considerados independientes.
	
	Utiliza la fórmula: H(X) = -Σ p(x) * log2(p(x))
	donde p(x) es la probabilidad de cada símbolo x.
	
	Args:
		data: Secuencia de datos a analizar
		
	Returns:
		float: Entropía en bits por símbolo
	"""
	probabilidades = calcular_probabilidades(data)
	return -sum(p * math.log2(p) for p in probabilidades.values())

def entropia_dependiente(data):
	"""
	Calcula la entropía considerando la dependencia entre pares de símbolos consecutivos.
	
	Analiza pares de símbolos (bigrams) para capturar correlaciones entre
	símbolos adyacentes, lo que puede revelar patrones en los datos.
	
	Args:
		data: Secuencia de datos a analizar
		
	Returns:
		float: Entropía de pares consecutivos en bits por símbolo
	"""
	# Crear pares de símbolos consecutivos (bigrams)
	pares = [(data[i], data[i+1]) for i in range(len(data)-1)]
	probabilidades = calcular_probabilidades(pares)
	return -sum(p * math.log2(p) for p in probabilidades.values())

def redundancia(entropia, num_simbolos):
	"""
	Calcula la redundancia de la información.
	
	La redundancia mide cuánta información "sobra" comparada con
	la distribución uniforme ideal.
	Fórmula: R = log2(N) - H
	donde N es el número de símbolos únicos y H es la entropía.
	
	Args:
		entropia (float): Entropía calculada
		num_simbolos (int): Número de símbolos únicos
		
	Returns:
		float: Redundancia en bits por símbolo
	"""
	return math.log2(num_simbolos) - entropia

def leer_archivo(ruta_archivo):
	"""
	Lee el contenido completo de un archivo en modo binario.
	
	Args:
		ruta_archivo (str): Ruta al archivo a leer
		
	Returns:
		bytes: Contenido del archivo como secuencia de bytes
	"""
	with open(ruta_archivo, 'rb') as file:
		return file.read()

def obtener_info_archivo(ruta_archivo, data):
	"""
	Extrae información básica del archivo analizado.
	
	Args:
		ruta_archivo (str): Ruta al archivo
		data (bytes): Datos del archivo
		
	Returns:
		dict: Información del archivo (nombre, tamaño, extensión)
	"""
	tamaño_bytes = len(data)
	tamaño_kb = tamaño_bytes / 1024  # Conversión a kilobytes
	nombre = os.path.basename(ruta_archivo)
	extension = os.path.splitext(ruta_archivo)[1]
	
	return {
		'nombre': nombre,
		'tamaño_bytes': tamaño_bytes,
		'tamaño_kb': round(tamaño_kb, 2),
		'extension': extension if extension else 'Sin extensión'
	}

def calcular_entropia_y_redundancia(ruta_archivo):
	"""
	Función principal que realiza el análisis completo de entropía de un archivo.
	
	Calcula tanto la entropía independiente (símbolos individuales) como
	la dependiente (pares consecutivos), junto con métricas derivadas como
	redundancia y eficiencia.
	
	Args:
		ruta_archivo (str): Ruta al archivo a analizar
		
	Returns:
		dict: Diccionario completo con todos los resultados del análisis
	"""
	inicio_tiempo = time.time()
	
	# Leer datos del archivo
	data = leer_archivo(ruta_archivo)
	num_simbolos = len(set(data))  # Contar símbolos únicos
	
	# Obtener información básica del archivo
	info_archivo = obtener_info_archivo(ruta_archivo, data)
	
	# Calcular entropía máxima teórica (distribución uniforme)
	entropia_maxima = math.log2(num_simbolos) if num_simbolos > 1 else 0
	estadisticas_basicas = {
		'total_bytes': len(data),
		'simbolos_unicos': num_simbolos,
		'entropia_maxima': entropia_maxima
	}
	
	# === ANÁLISIS INDEPENDIENTE ===
	# Calcular entropía tratando cada símbolo de forma independiente
	entropia_indep = entropia_independiente(data)
	redundancia_indep = redundancia(entropia_indep, num_simbolos)
	# Eficiencia: qué tan cerca está la entropía real de la máxima
	eficiencia_indep = (entropia_indep / entropia_maxima * 100) if entropia_maxima > 0 else 0
	# Entropía por bit: dividir entre 8 bits por byte
	entropia_por_bit_indep = entropia_indep / 8
	
	# === ANÁLISIS DEPENDIENTE ===
	# Calcular entropía considerando dependencias entre símbolos consecutivos
	entropia_dep = entropia_dependiente(data)
	redundancia_dep = redundancia(entropia_dep, num_simbolos)
	eficiencia_dep = (entropia_dep / entropia_maxima * 100) if entropia_maxima > 0 else 0
	entropia_por_bit_dep = entropia_dep / 8
	
	tiempo_procesamiento = time.time() - inicio_tiempo
	
	# Retornar todos los resultados organizados
	return {
		'info_archivo': info_archivo,
		'estadisticas_basicas': estadisticas_basicas,
		'tiempo_procesamiento': tiempo_procesamiento,
		'entropia_independiente': entropia_indep,
		'redundancia_independiente': redundancia_indep,
		'eficiencia_independiente': eficiencia_indep,
		'entropia_por_bit_independiente': entropia_por_bit_indep,
		'entropia_dependiente': entropia_dep,
		'redundancia_dependiente': redundancia_dep,
		'eficiencia_dependiente': eficiencia_dep,
		'entropia_por_bit_dependiente': entropia_por_bit_dep
	}

def main():
	"""
	Función principal del programa.
	
	Solicita al usuario el nombre de un archivo, lo analiza y muestra
	un reporte completo con estadísticas de entropía y redundancia.
	"""
	# Construir ruta base del directorio actual
	base_path = os.path.dirname(os.path.abspath(__file__)) + "/"
	nombre_archivo = base_path + input("Ingrese el nombre del archivo (con extensión): ")
	
	try:
		# Verificar que el archivo existe
		if os.path.exists(nombre_archivo):
			# Realizar análisis completo
			resultados = calcular_entropia_y_redundancia(nombre_archivo)
			info = resultados['info_archivo']
			stats = resultados['estadisticas_basicas']
			
			# === MOSTRAR INFORMACIÓN DEL ARCHIVO ===
			print(f"Archivo: {info['nombre']}")
			print(f"Tamaño: {info['tamaño_kb']} KB ({info['tamaño_bytes']} bytes)")
			print(f"Extensión: {info['extension']}")
			print(f"Tiempo de procesamiento: {resultados['tiempo_procesamiento']:.4f} segundos")
			print("-" * 60)
			
			# === MOSTRAR ESTADÍSTICAS BÁSICAS ===
			print("ESTADÍSTICAS BÁSICAS:")
			print(f"  Total de bytes: {stats['total_bytes']}")
			print(f"  Símbolos únicos: {stats['simbolos_unicos']}")
			print(f"  Entropía máxima: {stats['entropia_maxima']:.4f} bits/símbolo")
			
			# === MOSTRAR ANÁLISIS INDEPENDIENTE ===
			print("ANÁLISIS INDEPENDIENTE (símbolos individuales):")
			print(f"  Entropía: {resultados['entropia_independiente']:.4f} bits/símbolo")
			print(f"  Entropía por bit: {resultados['entropia_por_bit_independiente']:.4f}")
			print(f"  Redundancia: {resultados['redundancia_independiente']:.4f} bits/símbolo")
			print(f"  Eficiencia: {resultados['eficiencia_independiente']:.2f}%")
			
			# === MOSTRAR ANÁLISIS DEPENDIENTE ===
			print("ANÁLISIS DEPENDIENTE (pares consecutivos):")
			print(f"  Entropía: {resultados['entropia_dependiente']:.4f} bits/símbolo")
			print(f"  Entropía por bit: {resultados['entropia_por_bit_dependiente']:.4f}")
			print(f"  Redundancia: {resultados['redundancia_dependiente']:.4f} bits/símbolo")
			print(f"  Eficiencia: {resultados['eficiencia_dependiente']:.2f}%")
		else:
			print(f"Error: El archivo '{nombre_archivo}' no existe.")
			
	except Exception as e:
		print(f"Error al procesar el archivo: {e}")

# Punto de entrada del programa
if __name__ == "__main__":
	main()