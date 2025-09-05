"""
2. Escribir un programa en lenguaje a elección, que permita:
    a. Ingresar el nombre de un archivo con extensión .bmp
    b. Valide que el archivo sea con el formato adecuado.
    c. Muestre los datos de la cabecera del archivo .bmp
"""
import os
import struct

def leer_cabecera_bmp(nombre_archivo):
    """
    Lee y muestra la información de la cabecera de un archivo BMP.

    Args:
        nombre_archivo (str): La ruta al archivo .bmp.
    """
    # 1. Validar que el archivo sea .bmp y exista
    if not nombre_archivo.lower().endswith('.bmp'):
        print("Error: El archivo debe tener la extensión .bmp")
        return
    if not os.path.exists(nombre_archivo):
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        return

    print(f"--- Cabecera del Archivo BMP: {nombre_archivo} ---")

    with open(nombre_archivo, 'rb') as f:
        # 2. Leer la cabecera del archivo (14 bytes)
        signature = f.read(2).decode('utf-8')
        if signature != 'BM':
            print("Error: El archivo no es un BMP válido (la firma no es 'BM').")
            return
            
        file_size = struct.unpack('<i', f.read(4))[0]
        # Los siguientes 4 bytes están reservados
        f.read(4) 
        data_offset = struct.unpack('<i', f.read(4))[0]

        print("--- Cabecera Principal (14 bytes) ---")
        print(f"Firma: {signature}")
        print(f"Tamaño del Archivo: {file_size} bytes")
        print(f"Offset de Datos de Imagen: {data_offset}")

        # 3. Leer la cabecera de información de la imagen (DIB Header, 40 bytes)
        dib_header_size = struct.unpack('<i', f.read(4))[0]
        width = struct.unpack('<i', f.read(4))[0]
        height = struct.unpack('<i', f.read(4))[0]
        # Siguiente campo es planes (2 bytes)
        f.read(2)
        bit_count = struct.unpack('<h', f.read(2))[0]
        compression = struct.unpack('<i', f.read(4))[0]
        image_size = struct.unpack('<i', f.read(4))[0]
        x_pixels_per_m = struct.unpack('<i', f.read(4))[0]
        y_pixels_per_m = struct.unpack('<i', f.read(4))[0]
        colors_used = struct.unpack('<i', f.read(4))[0]
        colors_important = struct.unpack('<i', f.read(4))[0]
        
        print("\n--- Propiedades de la Imagen (40 bytes) ---")
        print(f"Tamaño de esta sección: {dib_header_size}")
        print(f"Ancho de la imagen: {width} píxeles")
        print(f"Alto de la imagen: {height} píxeles")
        print(f"Bits por Píxel: {bit_count}")
        print(f"Tipo de Compresión: {compression} (0=ninguna)")
        print(f"Tamaño de la imagen comprimida: {image_size} bytes")
        print(f"Resolución Horizontal: {x_pixels_per_m} px/m")
        print(f"Resolución Vertical: {y_pixels_per_m} px/m")
        print(f"Número de colores usados: {colors_used}")
        print(f"Número de colores importantes: {colors_important}")
        print("-" * 40)

# --- Inicio del programa ---
if __name__ == "__main__":
    nombre = input("Ingresa el nombre del archivo .bmp: ")
    leer_cabecera_bmp(nombre)