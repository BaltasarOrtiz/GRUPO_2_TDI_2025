import numpy as np
from scipy.optimize import minimize
"""
4. Desarrollar una aplicación de software que calcule la Capacidad de Canal de un canal R-ario Uniforme y NoUniforme. El soft debe aceptar como entrada el valor de R que identifica al canal (R= 2 Binario, R=3 Ternario
hasta R=4) los valores de probabilidades condicionales que representan la matriz del canal entregando como
salida el valor de las probabilidades independientes de cada uno de los símbolos de entrada que maximiza la
información mutua, esto es, lograr la capacidad de canal.
"""


class ChannelCapacityCalculator:
	"""
	Calculadora de capacidad de canal para canales discretos R-arios.
	
	Esta clase implementa el cálculo de la capacidad de canal de Shannon para canales
	discretos sin memoria, tanto con distribución uniforme como con distribución
	óptima de entrada.
	"""
	
	def __init__(self, R, channel_matrix):
		"""
		Inicializa la calculadora de capacidad de canal.
		
		Args:
			R (int): Número de símbolos del alfabeto de entrada/salida
					(2=binario, 3=ternario, 4=cuaternario, etc.)
			channel_matrix (list or np.array): Matriz R x R de probabilidades 
											 condicionales P(Y|X) donde cada elemento
											 (i,j) representa P(Y=j|X=i)
		
		Raises:
			ValueError: Si la matriz no tiene las dimensiones correctas o si
					   las filas no suman 1 (no es una matriz estocástica válida)
		"""
		self.R = R
		self.P_Y_given_X = np.array(channel_matrix)
		
		# Validar que la matriz tenga las dimensiones correctas
		if self.P_Y_given_X.shape != (R, R):
			raise ValueError(f"La matriz debe ser {R}x{R}")
		
		# Verificar que es una matriz estocástica válida (cada fila suma 1)
		row_sums = np.sum(self.P_Y_given_X, axis=1)
		if not np.allclose(row_sums, 1.0):
			raise ValueError("Cada fila de la matriz debe sumar 1")
	
	def entropy(self, probs):
		"""
		Calcula la entropía de Shannon para una distribución de probabilidad.
		
		La entropía se define como: H(X) = -Σ p(x) log₂ p(x)
		
		Args:
			probs (array-like): Vector de probabilidades
			
		Returns:
			float: Entropía en bits
		"""
		probs = np.array(probs)
		# Filtrar probabilidades cero para evitar log(0) = -∞
		probs = probs[probs > 0]
		return -np.sum(probs * np.log2(probs))
	
	def conditional_entropy(self, px):
		"""
		Calcula la entropía condicional H(Y|X).
		
		H(Y|X) = Σ p(x) H(Y|X=x) representa la incertidumbre promedio sobre Y
		cuando X es conocida.
		
		Args:
			px (array-like): Vector de probabilidades de entrada P(X)
			
		Returns:
			float: Entropía condicional en bits
		"""
		px = np.array(px)
		total_entropy = 0
		
		# Sumar sobre todos los símbolos de entrada
		for i in range(self.R):
			if px[i] > 0:  # Solo considerar símbolos con probabilidad positiva
				# Obtener la distribución condicional P(Y|X=i) (fila i de la matriz)
				conditional_probs = self.P_Y_given_X[i, :]
				# Calcular H(Y|X=i)
				h_y_given_xi = self.entropy(conditional_probs)
				# Ponderar por P(X=i)
				total_entropy += px[i] * h_y_given_xi
		
		return total_entropy
	
	def output_distribution(self, px):
		"""
		Calcula la distribución de probabilidad de salida P(Y).
		
		Usando la ley de probabilidad total: P(Y=j) = Σᵢ P(Y=j|X=i) * P(X=i)
		
		Args:
			px (array-like): Vector de probabilidades de entrada P(X)
			
		Returns:
			np.array: Vector de probabilidades de salida P(Y)
		"""
		px = np.array(px)
		# Multiplicación matriz-vector: cada componente j es Σᵢ P(Y=j|X=i) * P(X=i)
		return np.dot(px, self.P_Y_given_X)
	
	def mutual_information(self, px):
		"""
		Calcula la información mutua I(X;Y) entre entrada y salida.
		
		La información mutua mide cuánta información sobre X está contenida en Y.
		Se calcula como: I(X;Y) = H(Y) - H(Y|X)
		
		Args:
			px (array-like): Vector de probabilidades de entrada P(X)
			
		Returns:
			float: Información mutua en bits
		"""
		px = np.array(px)
		
		# Calcular H(Y): entropía de la distribución de salida
		py = self.output_distribution(px)
		h_y = self.entropy(py)
		
		# Calcular H(Y|X): entropía condicional
		h_y_given_x = self.conditional_entropy(px)
		
		# I(X;Y) = H(Y) - H(Y|X)
		return h_y - h_y_given_x
	
	def objective_function(self, px):
		"""
		Función objetivo para la optimización (negativo de la información mutua).
		
		Scipy.minimize busca mínimos, pero queremos maximizar I(X;Y),
		por lo que minimizamos -I(X;Y).
		
		Args:
			px (array-like): Vector de probabilidades de entrada a optimizar
			
		Returns:
			float: Negativo de la información mutua
		"""
		return -self.mutual_information(px)
	
	def calculate_capacity(self):
		"""
		Encuentra la capacidad del canal maximizando I(X;Y) sobre todas las
		distribuciones de entrada posibles.
		
		La capacidad es: C = max_{P(X)} I(X;Y)
		
		Returns:
			tuple: (capacidad_en_bits, distribución_óptima_de_entrada)
			
		Raises:
			RuntimeError: Si el algoritmo de optimización no converge
		"""
		
		# Restricción: la suma de probabilidades debe ser 1
		constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
		
		# Límites: cada probabilidad debe estar entre 0 y 1
		bounds = [(0, 1) for _ in range(self.R)]
		
		# Punto inicial: distribución uniforme (buena aproximación inicial)
		x0 = np.ones(self.R) / self.R
		
		# Optimización usando programación cuadrática secuencial
		result = minimize(self.objective_function, x0, 
						 method='SLSQP', bounds=bounds, constraints=constraints)
		
		if result.success:
			optimal_px = result.x
			capacity = -result.fun  # Convertir de vuelta a positivo
			return capacity, optimal_px
		else:
			raise RuntimeError("No se pudo encontrar la solución óptima")
	
	def calculate_uniform_capacity(self):
		"""
		Calcula la información mutua asumiendo distribución uniforme de entrada.
		
		Esta es una aproximación simple donde P(X=i) = 1/R para todo i.
		Generalmente es subóptima comparada con la distribución que maximiza
		la capacidad.
		
		Returns:
			tuple: (información_mutua_uniforme, distribución_uniforme)
		"""
		uniform_px = np.ones(self.R) / self.R
		return self.mutual_information(uniform_px), uniform_px
	
	def display_results(self):
		"""
		Muestra un resumen completo de los resultados de capacidad del canal.
		
		Presenta tanto la información mutua con distribución uniforme como
		la capacidad óptima del canal, junto con la ganancia obtenida.
		"""
		print(f"=== CANAL {self.R}-ARIO ===")
		print(f"Matriz del canal P(Y|X):")
		# Mostrar la matriz de transición del canal de forma legible
		for i, row in enumerate(self.P_Y_given_X):
			print(f"  X={i}: {[f'{p:.3f}' for p in row]}")
		
		# Calcular y mostrar resultados para distribución uniforme
		uniform_capacity, uniform_px = self.calculate_uniform_capacity()
		print(f"\n--- DISTRIBUCIÓN UNIFORME ---")
		print(f"Probabilidades de entrada: {[f'{p:.3f}' for p in uniform_px]}")
		print(f"Información mutua: {uniform_capacity:.4f} bits")
		
		# Calcular y mostrar la capacidad óptima del canal
		try:
			capacity, optimal_px = self.calculate_capacity()
			print(f"\n--- CAPACIDAD ÓPTIMA DEL CANAL ---")
			print(f"Probabilidades óptimas de entrada: {[f'{p:.4f}' for p in optimal_px]}")
			print(f"Capacidad del canal: {capacity:.4f} bits")
			print(f"Ganancia sobre distribución uniforme: {capacity - uniform_capacity:.4f} bits")
			
			# Calcular eficiencia del canal
			max_theoretical = np.log2(self.R)  # Capacidad teórica máxima
			efficiency = (capacity / max_theoretical) * 100
			print(f"Eficiencia del canal: {efficiency:.2f}% (de {max_theoretical:.4f} bits teóricos)")
			
		except RuntimeError as e:
			print(f"\nError en optimización: {e}")

def main():
	"""
	Función principal que demuestra el uso de la calculadora con diferentes
	tipos de canales (binario, ternario y cuaternario).
	"""
	print("Calculadora de Capacidad de Canal R-ario")
	print("========================================")
	print("Basada en la Teoría de la Información de Shannon")
	
	# Ejemplo 1: Canal binario asimétrico
	# Este canal tiene diferentes probabilidades de error para 0 y 1
	print("\nEjemplo 1: Canal Binario Asimétrico")
	print("(Probabilidades de error diferentes para cada símbolo)")
	matrix_binary = [
		[0.8, 0.2],   # P(Y=0|X=0)=0.8, P(Y=1|X=0)=0.2 - Error del 20% para X=0
		[0.25, 0.75]  # P(Y=0|X=1)=0.25, P(Y=1|X=1)=0.75 - Error del 25% para X=1
	]
	calc = ChannelCapacityCalculator(2, matrix_binary)
	calc.display_results()
	
	# Ejemplo 2: Canal ternario con ruido moderado
	print("\n" + "="*50)
	print("\nEjemplo 2: Canal Ternario con Ruido")
	print("(Cada símbolo puede confundirse con los otros con cierta probabilidad)")
	matrix_ternary = [
		[0.6, 0.3, 0.1],  # X=0 se recibe correctamente 60% de las veces
		[0.2, 0.5, 0.3],  # X=1 se recibe correctamente 50% de las veces
		[0.4, 0.2, 0.4]   # X=2 se recibe correctamente 40% de las veces
	]
	calc = ChannelCapacityCalculator(3, matrix_ternary)
	calc.display_results()
	
	# Ejemplo 3: Canal cuaternario casi simétrico
	print("\n" + "="*50)
	print("\nEjemplo 3: Canal Cuaternario (Casi Simétrico)")
	print("(Estructura casi diagonal - cada símbolo se confunde igualmente con otros)")
	matrix_quaternary = [
		[0.7, 0.1, 0.1, 0.1],  # X=0 correcto 70%, error distribuido uniformemente
		[0.1, 0.7, 0.1, 0.1],  # X=1 correcto 70%, error distribuido uniformemente
		[0.1, 0.1, 0.7, 0.1],  # X=2 correcto 70%, error distribuido uniformemente
		[0.1, 0.1, 0.1, 0.7]   # X=3 correcto 70%, error distribuido uniformemente
	]
	calc = ChannelCapacityCalculator(4, matrix_quaternary)
	calc.display_results()

if __name__ == "__main__":
	main()