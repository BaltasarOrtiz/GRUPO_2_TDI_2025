import struct
import os

def leer_cabecera_bmp(nombre_archivo):
    """
    Lee y muestra la información de la cabecera de un archivo BMP
    """
    try:
        # Verificar que el archivo existe
        if not os.path.exists(nombre_archivo):
            print(f"Error: El archivo '{nombre_archivo}' no existe.")
            return False
        
        # Verificar extensión
        if not nombre_archivo.lower().endswith('.bmp'):
            print("Error: El archivo debe tener extensión .bmp")
            return False
        
        with open(nombre_archivo, 'rb') as archivo:
            # Leer cabecera (14 bytes)
            cabecera = archivo.read(14)
            if len(cabecera) < 14:
                print("Error: Archivo demasiado pequeño para ser un BMP válido.")
                return False
            
            # Desempaquetar cabecera
            signature = cabecera[0:2].decode('ascii', errors='ignore')
            file_size = struct.unpack('<I', cabecera[2:6])[0]  # Little endian, unsigned int
            reserved = struct.unpack('<I', cabecera[6:10])[0]
            data_offset = struct.unpack('<I', cabecera[10:14])[0]
            
            # Validar signature
            if signature != 'BM':
                print(f"Error: Signature inválida '{signature}'. Debe ser 'BM'.")
                return False
            
            # Leer propiedades de la imagen (40 bytes)
            propiedades = archivo.read(40)
            if len(propiedades) < 40:
                print("Error: No se pudieron leer las propiedades de la imagen.")
                return False
            
            # Desempaquetar propiedades
            size = struct.unpack('<I', propiedades[0:4])[0]
            width = struct.unpack('<i', propiedades[4:8])[0]  # signed int
            height = struct.unpack('<i', propiedades[8:12])[0]  # signed int
            planes = struct.unpack('<H', propiedades[12:14])[0]  # unsigned short
            bit_count = struct.unpack('<H', propiedades[14:16])[0]
            compression = struct.unpack('<I', propiedades[16:20])[0]
            image_size = struct.unpack('<I', propiedades[20:24])[0]
            x_pixels_per_m = struct.unpack('<i', propiedades[24:28])[0]
            y_pixels_per_m = struct.unpack('<i', propiedades[28:32])[0]
            colors_used = struct.unpack('<I', propiedades[32:36])[0]
            colors_important = struct.unpack('<I', propiedades[36:40])[0]
            
            # Validaciones adicionales
            if size != 40:
                print(f"Warning: Tamaño de header inesperado: {size} bytes (esperado: 40)")
            
            if planes != 1:
                print(f"Warning: Número de planos inusual: {planes} (esperado: 1)")
            
            # Mostrar información
            print("="*50)
            print("INFORMACIÓN DE CABECERA BMP")
            print("="*50)
            print("\n--- CABECERA (14 bytes) ---")
            print(f"Signature:       {signature}")
            print(f"File Size:       {file_size:,} bytes")
            print(f"Reserved:        {reserved}")
            print(f"Data Offset:     {data_offset} bytes")
            
            print("\n--- PROPIEDADES DE IMAGEN (40 bytes) ---")
            print(f"Size:            {size} bytes")
            print(f"Width:           {width} píxeles")
            print(f"Height:          {height} píxeles")
            print(f"Planes:          {planes}")
            print(f"Bit Count:       {bit_count} bits por píxel")
            print(f"Compression:     {compression} ({'Sin compresión' if compression == 0 else 'Con compresión'})")
            print(f"Image Size:      {image_size:,} bytes")
            print(f"X Pixels/M:      {x_pixels_per_m}")
            print(f"Y Pixels/M:      {y_pixels_per_m}")
            print(f"Colors Used:     {colors_used}")
            print(f"Colors Important: {colors_important}")
            
            print("\n--- INFORMACIÓN ADICIONAL ---")
            print(f"Tamaño real archivo: {os.path.getsize(nombre_archivo):,} bytes")
            print(f"Resolución:      {width} x {abs(height)}")
            print(f"Tipo de color:   {obtener_tipo_color(bit_count)}")
            
            return True
            
    except FileNotFoundError:
        print(f"Error: No se puede abrir el archivo '{nombre_archivo}'")
        return False
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return False

def obtener_tipo_color(bit_count):
    """Devuelve una descripción del tipo de color según los bits por píxel"""
    tipos = {
        1: "Monocromático (2 colores)",
        4: "16 colores",
        8: "256 colores", 
        16: "65,536 colores (High Color)",
        24: "16,777,216 colores (True Color)",
        32: "16,777,216 colores + canal alfa"
    }
    return tipos.get(bit_count, f"Desconocido ({bit_count} bits)")

def main():
    """Función principal del programa"""
    print("ANALIZADOR DE ARCHIVOS BMP")
    print("=" * 30)
    base_path = os.path.dirname(os.path.abspath(__file__)) + "/"
    
    while True:
        # Solicitar nombre del archivo
        nombre_archivo = base_path + input("\nIngrese el nombre del archivo BMP (o 'salir' para terminar): ").strip()
        if nombre_archivo.lower() == 'salir':
            print("¡Hasta luego!")
            break
        
        if not nombre_archivo:
            print("Por favor, ingrese un nombre de archivo válido.")
            continue
        
        # Analizar el archivo
        exito = leer_cabecera_bmp(nombre_archivo)
        
        if exito:
            print("\n✓ Archivo analizado correctamente")
        else:
            print("\n✗ Error al analizar el archivo")
        
        print("-" * 50)

if __name__ == "__main__":
    main()