"""
7. Desarrollar un programa para comparar dos cadenas, no en forma tradicional (carácter por carácter), sino que implemente un algoritmo, propuesto por Ud., que determine el parecido, por ejemplo de cadenas como: Juan Perez y Jaun Perez, Horacio López y Oracio López, cadenas que si se tratan en comparando carácter por carácter, son muy poco parecidas o incluso no se parecen en nada.
"""
def calcular_distancia_levenshtein(s1, s2):
    """
    Calcula la distancia de Levenshtein entre dos cadenas.
    Este es el número mínimo de ediciones (inserción, eliminación, sustitución)
    para transformar s1 en s2.

    Args:
        s1 (str): La primera cadena.
        s2 (str): La segunda cadena.

    Returns:
        int: La distancia de Levenshtein.
    """
    m, n = len(s1), len(s2)
    # Creamos una matriz para almacenar las distancias parciales
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Llenamos la primera fila y la primera columna
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    # Calculamos la distancia para el resto de la matriz
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            coste = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1,        # Eliminación
                           dp[i][j - 1] + 1,        # Inserción
                           dp[i - 1][j - 1] + coste) # Sustitución

    return dp[m][n]

# --- Inicio del programa ---
if __name__ == "__main__":
    print("--- Calculadora de Similitud de Cadenas (Distancia de Levenshtein) ---")
    cadena1 = input("Ingresa la primera cadena (ej: Juan Perez): ")
    cadena2 = input("Ingresa la segunda cadena (ej: Jaun Perez): ")

    distancia = calcular_distancia_levenshtein(cadena1.lower(), cadena2.lower())

    # Normalizamos la distancia para obtener un porcentaje de similitud
    longitud_max = max(len(cadena1), len(cadena2))
    if longitud_max == 0:
        similitud = 100.0
    else:
        similitud = (1 - (distancia / longitud_max)) * 100

    print("\n--- Resultados ---")
    print(f"Distancia de Levenshtein: {distancia}")
    print(f"Las cadenas tienen una similitud del {similitud:.2f}%")