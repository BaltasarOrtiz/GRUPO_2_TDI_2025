import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt

class ChannelCapacityCalculator:
    def __init__(self, R, channel_matrix):
        """
        R: número de símbolos (2=binario, 3=ternario, 4=cuaternario)
        channel_matrix: matriz R x R de probabilidades condicionales P(Y|X)
        """
        self.R = R
        self.P_Y_given_X = np.array(channel_matrix)
        
        # Validar matriz
        if self.P_Y_given_X.shape != (R, R):
            raise ValueError(f"La matriz debe ser {R}x{R}")
        
        # Verificar que cada fila sume 1
        row_sums = np.sum(self.P_Y_given_X, axis=1)
        if not np.allclose(row_sums, 1.0):
            raise ValueError("Cada fila de la matriz debe sumar 1")
    
    def entropy(self, probs):
        """Calcula la entropía H(X) = -Σ p(x) log₂ p(x)"""
        probs = np.array(probs)
        probs = probs[probs > 0]  # Evitar log(0)
        return -np.sum(probs * np.log2(probs))
    
    def conditional_entropy(self, px):
        """Calcula H(Y|X) = Σ p(x) H(Y|X=x)"""
        px = np.array(px)
        total_entropy = 0
        
        for i in range(self.R):
            if px[i] > 0:
                # H(Y|X=i) para cada símbolo de entrada
                conditional_probs = self.P_Y_given_X[i, :]
                h_y_given_xi = self.entropy(conditional_probs)
                total_entropy += px[i] * h_y_given_xi
        
        return total_entropy
    
    def output_distribution(self, px):
        """Calcula P(Y) = Σ P(Y|X=x) * P(X=x)"""
        px = np.array(px)
        return np.dot(px, self.P_Y_given_X)
    
    def mutual_information(self, px):
        """Calcula I(X;Y) = H(Y) - H(Y|X)"""
        px = np.array(px)
        
        # H(Y)
        py = self.output_distribution(px)
        h_y = self.entropy(py)
        
        # H(Y|X)
        h_y_given_x = self.conditional_entropy(px)
        
        return h_y - h_y_given_x
    
    def objective_function(self, px):
        """Función objetivo para minimizar (negativo de I(X;Y))"""
        return -self.mutual_information(px)
    
    def calculate_capacity(self):
        """Encuentra la capacidad del canal maximizando I(X;Y)"""
        
        # Restricciones: Σ p(x) = 1 y p(x) ≥ 0
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = [(0, 1) for _ in range(self.R)]
        
        # Punto inicial: distribución uniforme
        x0 = np.ones(self.R) / self.R
        
        # Optimización
        result = minimize(self.objective_function, x0, 
                         method='SLSQP', bounds=bounds, constraints=constraints)
        
        if result.success:
            optimal_px = result.x
            capacity = -result.fun
            return capacity, optimal_px
        else:
            raise RuntimeError("No se pudo encontrar la solución óptima")
    
    def calculate_uniform_capacity(self):
        """Calcula la capacidad asumiendo distribución uniforme de entrada"""
        uniform_px = np.ones(self.R) / self.R
        return self.mutual_information(uniform_px), uniform_px
    
    def display_results(self):
        """Muestra los resultados de capacidad uniforme y no uniforme"""
        print(f"=== CANAL {self.R}-ARIO ===")
        print(f"Matriz del canal P(Y|X):")
        for i, row in enumerate(self.P_Y_given_X):
            print(f"  a{i+1}: {[f'{p:.3f}' for p in row]}")
        
        # Capacidad uniforme
        uniform_capacity, uniform_px = self.calculate_uniform_capacity()
        print(f"\n--- CANAL UNIFORME ---")
        print(f"Probabilidades de entrada: {[f'{p:.3f}' for p in uniform_px]}")
        print(f"Información mutua: {uniform_capacity:.4f} bits")
        
        # Capacidad óptima (no uniforme)
        try:
            capacity, optimal_px = self.calculate_capacity()
            print(f"\n--- CANAL NO UNIFORME (ÓPTIMO) ---")
            print(f"Probabilidades óptimas de entrada: {[f'{p:.4f}' for p in optimal_px]}")
            print(f"Capacidad del canal: {capacity:.4f} bits")
            print(f"Ganancia: {capacity - uniform_capacity:.4f} bits")
        except RuntimeError as e:
            print(f"\nError en optimización: {e}")

# Función principal para usar la calculadora
def main():
    print("Calculadora de Capacidad de Canal R-ario")
    print("========================================")
    
    # Ejemplo: Canal binario asimétrico
    print("\nEjemplo 1: Canal Binario Asimétrico")
    matrix_binary = [
        [0.8, 0.2],  # P(Y|X=0)
        [0.25, 0.75] # P(Y|X=1)
    ]
    calc = ChannelCapacityCalculator(2, matrix_binary)
    calc.display_results()
    
    # Ejemplo: Canal ternario
    print("\n" + "="*50)
    print("\nEjemplo 2: Canal Ternario")
    matrix_ternary = [
        [0.6, 0.3, 0.1],  # P(Y|X=0)
        [0.2, 0.5, 0.3],  # P(Y|X=1)
        [0.4, 0.2, 0.4]   # P(Y|X=2)
    ]
    calc = ChannelCapacityCalculator(3, matrix_ternary)
    calc.display_results()
    
    # Ejemplo: Canal cuaternario
    print("\n" + "="*50)
    print("\nEjemplo 3: Canal Cuaternario")
    matrix_quaternary = [
        [0.7, 0.1, 0.1, 0.1],  # P(Y|X=0)
        [0.1, 0.7, 0.1, 0.1],  # P(Y|X=1)
        [0.1, 0.1, 0.7, 0.1],  # P(Y|X=2)
        [0.1, 0.1, 0.1, 0.7]   # P(Y|X=3)
    ]
    calc = ChannelCapacityCalculator(4, matrix_quaternary)
    calc.display_results()

if __name__ == "__main__":
    main()