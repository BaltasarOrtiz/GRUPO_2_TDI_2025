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

    # 2. Validar que el archivo tenga el formato BMP correcto antes de procesarlo
    try:
        with open(nombre_archivo, 'rb') as f:
            # Verificar que el archivo tenga al menos 54 bytes para la cabecera BMP básica
            if os.path.getsize(nombre_archivo) < 54:
                print("Error: El archivo es demasiado pequeño para ser un archivo BMP válido.")
                return
            
            # Leer los primeros 2 bytes para validar la firma BMP
            signature_bytes = f.read(2)
            if len(signature_bytes) < 2:
                print("Error: No se pudo leer la cabecera del archivo.")
                return
            
            signature = signature_bytes.decode('utf-8', errors='ignore')
            
            if signature != 'BM':
                print("Error: El archivo no es un archivo BMP válido.")
                print(f"Se esperaba 'BM', pero se encontró '{signature}'")
                return
    except Exception as e:
        print(f"Error al validar el archivo: {e}")
        return

    print(f"--- Cabecera del Archivo BMP: {nombre_archivo} ---")

    with open(nombre_archivo, 'rb') as f:
        # 3. Leer la cabecera del archivo (14 bytes)
        signature = f.read(2).decode('utf-8')
            
        file_size = struct.unpack('<i', f.read(4))[0]
        # Los siguientes 4 bytes están reservados
        reserved = struct.unpack('<i', f.read(4))[0]
        data_offset = struct.unpack('<i', f.read(4))[0]

        print("--- Cabecera Principal (14 bytes) ---")
        print(f"Signature: {signature}")
        print(f"FileSize: {file_size} bytes")
        print(f"Reserved: {reserved}")
        print(f"DataOffset: {data_offset}")

        # 4. Leer la cabecera de información de la imagen (DIB Header, 40 bytes)
        dib_header_size = struct.unpack('<i', f.read(4))[0]
        width = struct.unpack('<i', f.read(4))[0]
        height = struct.unpack('<i', f.read(4))[0]
        # Siguiente campo es planes (2 bytes)
        planes = struct.unpack('<h', f.read(2))[0]
        bit_count = struct.unpack('<h', f.read(2))[0]
        compression = struct.unpack('<i', f.read(4))[0]
        image_size = struct.unpack('<i', f.read(4))[0]
        x_pixels_per_m = struct.unpack('<i', f.read(4))[0]
        y_pixels_per_m = struct.unpack('<i', f.read(4))[0]
        colors_used = struct.unpack('<i', f.read(4))[0]
        colors_important = struct.unpack('<i', f.read(4))[0]
        
        print("\n--- Propiedades de la Imagen (40 bytes) ---")
        print(f"Size: {dib_header_size} bytes")
        print(f"Width: {width} píxeles")
        print(f"Height: {height} píxeles")
        print(f"Planes: {planes}")
        print(f"BitCount: {bit_count} bits por píxel")
        print(f"Compression: {compression} (0=ninguna, 1=RLE-8, 2=RLE-4)")
        print(f"ImageSize: {image_size} bytes")
        print(f"XPixelsPerM: {x_pixels_per_m} píxeles por metro")
        print(f"YPixelsPerM: {y_pixels_per_m} píxeles por metro")
        print(f"ColorsUsed: {colors_used}")
        print(f"ColorsImportant: {colors_important}")
        print("-" * 40)

# --- Inicio del programa ---
if __name__ == "__main__":
    nombre = input("Ingresa el nombre del archivo .bmp: ")
    leer_cabecera_bmp(nombre)