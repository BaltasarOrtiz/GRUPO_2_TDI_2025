"""
4. Desarrollar una aplicación de software que calcule la Capacidad de Canal de un canal R-ario Uniforme y NoUniforme. El soft debe aceptar como entrada el valor de R que identifica al canal (R= 2 Binario, R=3 Ternario hasta R=4) los valores de probabilidades condicionales que representan la matriz del canal entregando como salida el valor de las probabilidades independientes de cada uno de los símbolos de entrada que maximiza la información mutua, esto es, lograr la capacidad de canal.
"""
import numpy as np
import math

def calcular_capacidad_canal(matriz_canal, tolerancia=1e-5, max_iter=1000):
    """
    Calcula la capacidad de un canal discreto sin memoria usando el algoritmo de Blahut-Arimoto.

    Args:
        matriz_canal (np.array): Matriz de probabilidades P(y|x), 
                                 donde las filas son las entradas (x) y 
                                 las columnas son las salidas (y).
        tolerancia (float): Criterio de parada para la convergencia.
        max_iter (int): Número máximo de iteraciones.
        
    Returns:
        tuple: (capacidad, distribucion_optima)
    """
    # Validar que la matriz sea estocástica por filas
    if not np.allclose(matriz_canal.sum(axis=1), 1):
        raise ValueError("Las filas de la matriz del canal deben sumar 1.")

    num_entradas, num_salidas = matriz_canal.shape
    
    # 1. Iniciar con una distribución de entrada uniforme
    p_x = np.full(num_entradas, 1 / num_entradas)
    
    for i in range(max_iter):
        # 2. Calcular P(y) y P(x|y)
        p_y = p_x @ matriz_canal
        p_xy = matriz_canal * p_x[:, np.newaxis] # P(x,y) = P(y|x) * P(x)
        
        # Evitar división por cero si alguna salida tiene probabilidad 0
        p_y[p_y == 0] = 1e-10
        
        p_x_dado_y = p_xy / p_y # P(x|y) = P(x,y) / P(y)

        # 3. Calcular c(x) para la actualización de p(x)
        # Usamos logaritmos base 2 para obtener el resultado en bits
        # D(P(y|x) || P(y)) = sum_y P(y|x) * log2(P(y|x) / P(y))
        # Para evitar log(0), añadimos un valor muy pequeño (epsilon)
        epsilon = 1e-12
        c_x = np.exp(np.sum(matriz_canal * np.log2((matriz_canal + epsilon) / (p_y + epsilon)), axis=1))
        
        # 4. Actualizar p(x)
        p_x_nuevo = p_x * c_x
        p_x_nuevo /= np.sum(p_x_nuevo) # Normalizar para que sume 1
        
        # 5. Comprobar la convergencia
        if np.linalg.norm(p_x_nuevo - p_x) < tolerancia:
            print(f"Convergencia alcanzada en la iteración {i+1}.")
            break
            
        p_x = p_x_nuevo
    else:
        print("Se alcanzó el número máximo de iteraciones.")

    # 6. Calcular la capacidad con la distribución óptima encontrada
    # Capacidad C = I(X;Y) = sum_{x,y} p(x)p(y|x) * log2(p(y|x)/p(y))
    p_y_final = p_x @ matriz_canal
    capacidad = np.sum(p_x[:, np.newaxis] * matriz_canal * np.log2((matriz_canal + epsilon) / (p_y_final + epsilon)))
    
    return capacidad, p_x

# --- Inicio del programa ---
if __name__ == "__main__":
    try:
        R = int(input("Introduce el valor de R (número de símbolos de entrada, ej: 2, 3, 4): "))
        if R <= 1:
            raise ValueError("R debe ser mayor que 1.")
            
        print(f"\nIntroduce la matriz de probabilidades del canal P(salida|entrada) de {R}xR.")
        print("Ingresa los valores de cada fila separados por espacios.")
        
        filas = []
        for i in range(R):
            while True:
                fila_str = input(f"Fila {i+1}: ")
                try:
                    fila = [float(val) for val in fila_str.split()]
                    if len(fila) != R:
                        print(f"Error: La fila debe tener {R} valores.")
                    elif not math.isclose(sum(fila), 1.0):
                        print("Error: La suma de las probabilidades de la fila debe ser 1.")
                    else:
                        filas.append(fila)
                        break
                except ValueError:
                    print("Error: Ingresa solo números válidos.")

        matriz = np.array(filas)
        
        capacidad, distribucion = calcular_capacidad_canal(matriz)
        
        print("\n--- Resultados ---")
        print(f"Capacidad del Canal (C): {capacidad:.4f} bits/símbolo")
        print("Distribución de probabilidad de entrada que maximiza la capacidad:")
        for i, p in enumerate(distribucion):
            print(f"  P(a{i+1}) = {p:.4f}")
            
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")