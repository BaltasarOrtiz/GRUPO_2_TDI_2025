import math
import os
import time
from collections import Counter

def calcular_probabilidades(data):
	"""Calcula las probabilidades de cada símbolo en los datos."""
	total = len(data)
	frecuencias = Counter(data)
	return {char: freq / total for char, freq in frecuencias.items()}

def entropia_independiente(data):
	"""Calcula la entropía de los símbolos considerados de forma independiente."""
	probabilidades = calcular_probabilidades(data)
	return -sum(p * math.log2(p) for p in probabilidades.values())

def entropia_dependiente(data):
	"""Calcula la entropía considerando la dependencia entre pares de símbolos consecutivos."""
	pares = [(data[i], data[i+1]) for i in range(len(data)-1)]
	probabilidades = calcular_probabilidades(pares)
	return -sum(p * math.log2(p) for p in probabilidades.values())

def redundancia(entropia, num_simbolos):
	"""Calcula la redundancia utilizando la fórmula: log2(N) - H."""
	return math.log2(num_simbolos) - entropia

def leer_archivo(ruta_archivo):
	"""Lee el contenido del archivo en modo binario."""
	with open(ruta_archivo, 'rb') as file:
		return file.read()

def obtener_info_archivo(ruta_archivo, data):
	"""Obtiene información básica del archivo."""
	tamaño_bytes = len(data)
	tamaño_kb = tamaño_bytes / 1024
	nombre = os.path.basename(ruta_archivo)
	extension = os.path.splitext(ruta_archivo)[1]
	
	return {
		'nombre': nombre,
		'tamaño_bytes': tamaño_bytes,
		'tamaño_kb': round(tamaño_kb, 2),
		'extension': extension if extension else 'Sin extensión'
	}

def calcular_entropia_y_redundancia(ruta_archivo):
	"""Lee los datos del archivo y calcula la entropía y la redundancia."""
	inicio_tiempo = time.time()
	
	data = leer_archivo(ruta_archivo)
	num_simbolos = len(set(data))
	
	# Información del archivo
	info_archivo = obtener_info_archivo(ruta_archivo, data)
	
	# Estadísticas básicas
	entropia_maxima = math.log2(num_simbolos) if num_simbolos > 1 else 0
	estadisticas_basicas = {
		'total_bytes': len(data),
		'simbolos_unicos': num_simbolos,
		'entropia_maxima': entropia_maxima
	}
	
	# Cálculos de entropía independiente
	entropia_indep = entropia_independiente(data)
	redundancia_indep = redundancia(entropia_indep, num_simbolos)
	eficiencia_indep = (entropia_indep / entropia_maxima * 100) if entropia_maxima > 0 else 0
	entropia_por_bit_indep = entropia_indep / 8
	
	# Cálculos de entropía dependiente
	entropia_dep = entropia_dependiente(data)
	redundancia_dep = redundancia(entropia_dep, num_simbolos)
	eficiencia_dep = (entropia_dep / entropia_maxima * 100) if entropia_maxima > 0 else 0
	entropia_por_bit_dep = entropia_dep / 8
	
	tiempo_procesamiento = time.time() - inicio_tiempo
	
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
	"""Función principal del programa."""
	base_path = os.path.dirname(os.path.abspath(__file__)) + "/"
	nombre_archivo = base_path + input("Ingrese el nombre del archivo (con extensión): ")
	
	try:
		if os.path.exists(nombre_archivo):
			resultados = calcular_entropia_y_redundancia(nombre_archivo)
			info = resultados['info_archivo']
			stats = resultados['estadisticas_basicas']
			
			print(f"Archivo: {info['nombre']}")
			print(f"Tamaño: {info['tamaño_kb']} KB ({info['tamaño_bytes']} bytes)")
			print(f"Extensión: {info['extension']}")
			print(f"Tiempo de procesamiento: {resultados['tiempo_procesamiento']:.4f} segundos")
			print("-" * 60)
			
			print("ESTADÍSTICAS BÁSICAS:")
			print(f"  Total de bytes: {stats['total_bytes']}")
			print(f"  Símbolos únicos: {stats['simbolos_unicos']}")
			print(f"  Entropía máxima: {stats['entropia_maxima']:.4f} bits/símbolo")
			
			print("ANÁLISIS INDEPENDIENTE (símbolos individuales):")
			print(f"  Entropía: {resultados['entropia_independiente']:.4f} bits/símbolo")
			print(f"  Entropía por bit: {resultados['entropia_por_bit_independiente']:.4f}")
			print(f"  Redundancia: {resultados['redundancia_independiente']:.4f} bits/símbolo")
			print(f"  Eficiencia: {resultados['eficiencia_independiente']:.2f}%")
			
			print("ANÁLISIS DEPENDIENTE (pares consecutivos):")
			print(f"  Entropía: {resultados['entropia_dependiente']:.4f} bits/símbolo")
			print(f"  Entropía por bit: {resultados['entropia_por_bit_dependiente']:.4f}")
			print(f"  Redundancia: {resultados['redundancia_dependiente']:.4f} bits/símbolo")
			print(f"  Eficiencia: {resultados['eficiencia_dependiente']:.2f}%")
		else:
			print(f"Error: El archivo '{nombre_archivo}' no existe.")
			
	except Exception as e:
		print(f"Error al procesar el archivo: {e}")

if __name__ == "__main__":
	main()