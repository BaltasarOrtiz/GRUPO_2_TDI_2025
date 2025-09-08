"""
7. Desarrollar un programa para comparar dos cadenas, no en forma tradicional (carácter por carácter), sino que
implemente un algoritmo, propuesto por Ud., que determine el parecido, por ejemplo de cadenas como: Juan
Perez y Jaun Perez, Horacio López y Oracio López, cadenas que si se tratan en comparando carácter por
carácter, son muy poco parecidas o incluso no se parecen en nada.
"""

class JaroWinkler:
	"""
	Implementación del algoritmo Jaro-Winkler para medir la similitud entre cadenas.
	
	El algoritmo Jaro-Winkler es especialmente útil para detectar errores tipográficos
	y variaciones menores en nombres y cadenas de texto, ya que da mayor peso a los
	caracteres coincidentes al inicio de las cadenas.
	"""
	
	# Umbral mínimo de similitud Jaro para aplicar el ajuste de Winkler
	threshold = 0.7
	
	# Divisor para el cálculo de la fórmula de Jaro (siempre es 3)
	three = 3
	
	# Coeficiente de escalamiento para el ajuste de Winkler (máximo 0.25)
	jw_coef = 0.1

	def similarity(self, s0, s1):
		"""
		Calcula la similitud Jaro-Winkler entre dos cadenas.
		
		La fórmula de Jaro es: (m/|s1| + m/|s2| + (m-t)/m) / 3
		donde m = coincidencias, t = transposiciones
		
		El ajuste de Winkler añade: Jaro + (L * P * (1 - Jaro))
		donde L = longitud del prefijo común, P = coeficiente de escalamiento
		
		:param s0: Primera cadena a comparar
		:param s1: Segunda cadena a comparar
		:return: Valor de similitud entre 0.0 (no similares) y 1.0 (idénticas)
		"""
		# Caso especial: cadenas idénticas
		if s0 == s1: 
			return 1.0
		
		# Obtiene estadísticas de coincidencias entre las cadenas
		mtp = self.matches(s0, s1)
		m = mtp[0]  # Número de caracteres coincidentes
		
		# Si no hay coincidencias, las cadenas no son similares
		if m == 0: 
			return 0.0
		
		# Calcula la similitud base usando la fórmula de Jaro
		# m/len(s0): proporción de coincidencias en s0
		# m/len(s1): proporción de coincidencias en s1  
		# (m-t)/m: proporción de coincidencias sin transposiciones
		j = (m / len(s0) + m / len(s1) + (m - mtp[1]) / m) / self.three
		jw = j
		
		# Aplica el ajuste de Winkler si la similitud Jaro supera el umbral
		if j > self.threshold:
			# Calcula el factor de escalamiento basado en el prefijo común
			prefix_scale = min(self.jw_coef, 1.0 / mtp[self.three])
			# Aplica la mejora de Winkler: da bonificación por prefijo común
			jw = j + prefix_scale * mtp[2] * (1 - j)
			
		return jw

	@staticmethod
	def matches(s0, s1):
		"""
		Encuentra las coincidencias y transposiciones entre dos cadenas según Jaro.
		
		Dos caracteres coinciden si:
		1. Son iguales
		2. Están dentro del rango permitido: max(len(cadena_larga)/2 - 1, 0)
		
		Una transposición ocurre cuando dos caracteres coincidentes están
		en diferente orden en sus respectivas secuencias de coincidencias.
		
		:param s0: Primera cadena a comparar
		:param s1: Segunda cadena a comparar
		:return: Lista con [coincidencias, transposiciones, prefijo_común, longitud_máxima]
		"""
		# Identifica la cadena más larga para optimizar la búsqueda
		if len(s0) > len(s1):
			max_str, min_str = s0, s1
		else:
			max_str, min_str = s1, s0

		# Calcula el rango de búsqueda permitido (ventana de coincidencias)
		# Según Jaro: máximo la mitad de la longitud de la cadena más larga menos 1
		ran = max(int(len(max_str) / 2 - 1), 0)
		
		# Estructuras para rastrear las coincidencias
		match_indexes = [-1] * len(min_str)  # Índices de coincidencias en min_str
		match_flags = [False] * len(max_str)  # Banderas de caracteres ya emparejados
		matches = 0
		
		# Busca coincidencias dentro del rango permitido
		for mi in range(len(min_str)):
			c1 = min_str[mi]  # Carácter actual de la cadena menor
			
			# Define la ventana de búsqueda alrededor de la posición actual
			inicio = max(mi - ran, 0)
			fin = min(mi + ran + 1, len(max_str))
			
			# Busca el carácter en la ventana de la cadena mayor
			for xi in range(inicio, fin):
				if not match_flags[xi] and c1 == max_str[xi]:
					match_indexes[mi] = xi  # Registra dónde se encontró la coincidencia
					match_flags[xi] = True  # Marca el carácter como emparejado
					matches += 1
					break  # Solo una coincidencia por carácter

		# Construye las secuencias de caracteres coincidentes para contar transposiciones
		ms0, ms1 = [0] * matches, [0] * matches
		
		# Extrae los caracteres coincidentes de min_str en orden
		si = 0
		for i in range(len(min_str)):
			if match_indexes[i] != -1:
				ms0[si] = min_str[i]
				si += 1

		# Extrae los caracteres coincidentes de max_str en orden
		si = 0
		for j in range(len(max_str)):
			if match_flags[j]:
				ms1[si] = max_str[j]
				si += 1

		# Cuenta las transposiciones: caracteres coincidentes en diferente orden
		transpositions = sum(ms0[mi] != ms1[mi] for mi in range(len(ms0)))

		# Calcula la longitud del prefijo común (hasta 4 caracteres máximo)
		prefix = 0
		for mi in range(min(len(s0), len(s1), 4)):
			if s0[mi] != s1[mi]: 
				break
			prefix += 1
			
		# Retorna: [coincidencias, transposiciones/2, prefijo_común, longitud_máxima]
		# Las transposiciones se dividen por 2 porque cada transposición involucra 2 caracteres
		return [matches, int(transpositions / 2), prefix, len(max_str)]


# Demostración del algoritmo con los ejemplos proporcionados
print("=== Comparación de similitud usando Jaro-Winkler ===")

# Ejemplo 1: Error tipográfico común (intercambio de caracteres)
string1 = "Juan Perez"
string2 = "Jaun Perez"
similitud1 = JaroWinkler().similarity(string1, string2)
print(f"'{string1}' vs '{string2}': {similitud1:.4f}")

# Ejemplo 2: Omisión de carácter al inicio
string1 = "Horacio López"
string2 = "Oracio López"
similitud2 = JaroWinkler().similarity(string1, string2)
print(f"'{string1}' vs '{string2}': {similitud2:.4f}")

print(f"\nAmbas cadenas muestran alta similitud a pesar de los errores tipográficos.")