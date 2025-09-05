"""
3. Desarrollar una aplicación de software que calcule la entropía y redundancia, de una fuente con símbolos vistos en forma independiente y dependiente en O(1). Realizar comparaciones para diferentes archivos (*.txt, *.exe, *.zip etc.)
"""
import math
import os
from collections import Counter

def calcular_entropia(nombre_archivo):
    """
    Calcula la entropía y redundancia de un archivo dado.

    Args:
        nombre_archivo (str): La ruta al archivo.
    """
    if not os.path.exists(nombre_archivo):
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        return

    print(f"--- Análisis de Entropía para: {nombre_archivo} ---")

    # 1. Leer el archivo en modo binario
    with open(nombre_archivo, 'rb') as f:
        contenido_bytes = f.read()

    tamano_total = len(contenido_bytes)
    if tamano_total == 0:
        print("El archivo está vacío. No se puede calcular la entropía.")
        return
        
    print(f"Tamaño del archivo: {tamano_total} bytes")

    # 2. Contar la frecuencia de cada byte (símbolo)
    # Counter es una herramienta muy eficiente para esto.
    frecuencias = Counter(contenido_bytes)

    # 3. Calcular la entropía de la fuente (orden 0)
    entropia = 0.0
    for byte_val in frecuencias:
        # Probabilidad = (veces que aparece el byte) / (total de bytes)
        probabilidad = frecuencias[byte_val] / tamano_total
        # Fórmula de Entropía de Shannon
        entropia -= probabilidad * math.log2(probabilidad)
    
    # La entropía se mide en bits por símbolo (en este caso, por byte)
    print(f"Entropía de la fuente (H): {entropia:.4f} bits/byte")

    # 4. Calcular la redundancia
    # La entropía máxima para una fuente de 256 símbolos (0-255) es log2(256) = 8
    entropia_maxima = 8.0
    # Redundancia = 1 - (Entropía real / Entropía máxima)
    redundancia = 1 - (entropia / entropia_maxima)

    print(f"Entropía Máxima posible: {entropia_maxima:.4f} bits/byte")
    print(f"Redundancia: {redundancia:.4f} (o {redundancia*100:.2f}%)")
    print("-" * 40)
    
    # Conclusión simple
    if redundancia > 0.5:
        print("El archivo tiene una alta redundancia, lo que sugiere que es muy compresible.")
    elif redundancia < 0.1:
         print("El archivo tiene una baja redundancia, probablemente ya está comprimido o encriptado.")
    else:
        print("El archivo tiene una redundancia moderada.")


# --- Inicio del programa ---
if __name__ == "__main__":
    nombre = input("Ingresa el nombre de cualquier archivo para analizar: ")
    calcular_entropia(nombre)