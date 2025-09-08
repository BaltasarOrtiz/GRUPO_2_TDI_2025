import struct
import os
"""
2. Escribir un programa en lenguaje a elección, que permita:
a. Ingresar el nombre de un archivo con extensión .bmp
b. Valide que el archivo sea con el formato adecuado.
c. Muestre los datos de la cabecera del archivo .bmp
"""

def leer_cabecera_bmp(nombre_archivo):
	"""
	Lee y muestra la información de la cabecera de un archivo BMP.
	
	Un archivo BMP tiene la siguiente estructura:
	- Cabecera de archivo (14 bytes): información general del archivo
	- Cabecera de información (40 bytes): propiedades de la imagen
	- Datos de la imagen: píxeles de la imagen
	
	Args:
		nombre_archivo (str): Ruta al archivo BMP a analizar
		
	Returns:
		bool: True si el análisis fue exitoso, False en caso contrario
	"""
	try:
		# Validación 1: Verificar que el archivo existe en el sistema
		if not os.path.exists(nombre_archivo):
			print(f"Error: El archivo '{nombre_archivo}' no existe.")
			return False
		
		# Validación 2: Verificar que tiene extensión .bmp
		if not nombre_archivo.lower().endswith('.bmp'):
			print("Error: El archivo debe tener extensión .bmp")
			return False
		
		with open(nombre_archivo, 'rb') as archivo:
			# PASO 1: Leer la cabecera de archivo BMP (primeros 14 bytes)
			# Esta cabecera contiene información básica sobre el archivo
			cabecera = archivo.read(14)
			if len(cabecera) < 14:
				print("Error: Archivo demasiado pequeño para ser un BMP válido.")
				return False
			
			# PASO 2: Desempaquetar los campos de la cabecera de archivo
			# Formato BMP usa little-endian para números de múltiples bytes
			
			# Bytes 0-1: Signature "BM" (identifica el archivo como BMP)
			signature = cabecera[0:2].decode('ascii', errors='ignore')
			
			# Bytes 2-5: Tamaño total del archivo en bytes (unsigned int 32-bit)
			file_size = struct.unpack('<I', cabecera[2:6])[0]  # <I = little endian unsigned int
			
			# Bytes 6-9: Campo reservado (debe ser 0)
			reserved = struct.unpack('<I', cabecera[6:10])[0]
			
			# Bytes 10-13: Offset donde comienzan los datos de píxeles
			data_offset = struct.unpack('<I', cabecera[10:14])[0]
			
			# Validación 3: Verificar que la signature sea correcta
			if signature != 'BM':
				print(f"Error: Signature inválida '{signature}'. Debe ser 'BM'.")
				return False
			
			# PASO 3: Leer la cabecera de información de imagen (siguientes 40 bytes)
			# Esta cabecera contiene las propiedades específicas de la imagen
			propiedades = archivo.read(40)
			if len(propiedades) < 40:
				print("Error: No se pudieron leer las propiedades de la imagen.")
				return False
			
			# PASO 4: Desempaquetar los campos de la cabecera de información
			
			# Bytes 0-3: Tamaño de esta cabecera (debe ser 40 para BMP estándar)
			size = struct.unpack('<I', propiedades[0:4])[0]
			
			# Bytes 4-7: Ancho de la imagen en píxeles (signed int, puede ser negativo)
			width = struct.unpack('<i', propiedades[4:8])[0]  # <i = little endian signed int
			
			# Bytes 8-11: Alto de la imagen en píxeles (signed int)
			# Si es positivo: imagen invertida (bottom-up), si es negativo: normal (top-down)
			height = struct.unpack('<i', propiedades[8:12])[0]
			
			# Bytes 12-13: Número de planos de color (debe ser 1)
			planes = struct.unpack('<H', propiedades[12:14])[0]  # <H = little endian unsigned short
			
			# Bytes 14-15: Bits por píxel (profundidad de color)
			bit_count = struct.unpack('<H', propiedades[14:16])[0]
			
			# Bytes 16-19: Tipo de compresión (0 = sin compresión)
			compression = struct.unpack('<I', propiedades[16:20])[0]
			
			# Bytes 20-23: Tamaño de los datos de imagen en bytes
			image_size = struct.unpack('<I', propiedades[20:24])[0]
			
			# Bytes 24-27: Resolución horizontal en píxeles por metro
			x_pixels_per_m = struct.unpack('<i', propiedades[24:28])[0]
			
			# Bytes 28-31: Resolución vertical en píxeles por metro
			y_pixels_per_m = struct.unpack('<i', propiedades[28:32])[0]
			
			# Bytes 32-35: Número de colores usados en la paleta
			colors_used = struct.unpack('<I', propiedades[32:36])[0]
			
			# Bytes 36-39: Número de colores importantes (0 = todos)
			colors_important = struct.unpack('<I', propiedades[36:40])[0]
			
			# PASO 5: Validaciones adicionales de consistencia
			
			# Verificar que el tamaño de la cabecera sea el estándar
			if size != 40:
				print(f"Warning: Tamaño de header inesperado: {size} bytes (esperado: 40)")
			
			# Verificar que el número de planos sea correcto
			if planes != 1:
				print(f"Warning: Número de planos inusual: {planes} (esperado: 1)")
			
			# PASO 6: Mostrar toda la información extraída de forma organizada
			print("="*50)
			print("INFORMACIÓN DE CABECERA BMP")
			print("="*50)
			
			# Información de la cabecera de archivo
			print("\n--- CABECERA DE ARCHIVO (14 bytes) ---")
			print(f"Signature:       {signature}")
			print(f"File Size:       {file_size:,} bytes")
			print(f"Reserved:        {reserved}")
			print(f"Data Offset:     {data_offset} bytes")
			
			# Información de la cabecera de imagen
			print("\n--- CABECERA DE IMAGEN (40 bytes) ---")
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
			
			# Información calculada y adicional
			print("\n--- INFORMACIÓN CALCULADA ---")
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
	"""
	Devuelve una descripción del tipo de color según los bits por píxel.
	
	En BMP, la profundidad de color determina cuántos colores diferentes
	se pueden representar:
	- 1 bit: 2 colores (monocromático)
	- 4 bits: 16 colores 
	- 8 bits: 256 colores
	- 16 bits: 65,536 colores (High Color)
	- 24 bits: 16,777,216 colores (True Color)
	- 32 bits: True Color + canal alfa (transparencia)
	
	Args:
		bit_count (int): Número de bits por píxel
		
	Returns:
		str: Descripción del tipo de color
	"""
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
	"""
	Función principal del programa.
	
	Implementa un bucle interactivo que permite al usuario:
	1. Ingresar nombres de archivos BMP para analizar
	2. Ver la información de cabecera de cada archivo
	3. Salir del programa cuando desee
	
	Los archivos se buscan en el mismo directorio que este script.
	"""
	print("ANALIZADOR DE ARCHIVOS BMP")
	print("=" * 30)
	
	# Obtener la ruta del directorio donde está este script
	# Esto permite buscar archivos BMP en la misma carpeta
	base_path = os.path.dirname(os.path.abspath(__file__)) + "/"
	
	# Bucle principal del programa
	while True:
		# Solicitar nombre del archivo al usuario
		nombre_archivo = input("\nIngrese el nombre del archivo BMP (o 'salir' para terminar): ").strip()
		
		# Verificar si el usuario quiere salir
		if nombre_archivo.lower() == 'salir':
			print("¡Hasta luego!")
			break
		
		# Validar que se ingresó un nombre
		if not nombre_archivo:
			print("Por favor, ingrese un nombre de archivo válido.")
			continue
		
		# Construir la ruta completa al archivo
		ruta_completa = base_path + nombre_archivo
		
		# Analizar el archivo BMP
		exito = leer_cabecera_bmp(ruta_completa)
		
		# Mostrar resultado del análisis
		if exito:
			print("\n✓ Archivo analizado correctamente")
		else:
			print("\n✗ Error al analizar el archivo")
		
		print("-" * 50)

# Punto de entrada del programa
# Solo ejecuta main() si este archivo se ejecuta directamente
# (no si se importa como módulo)
if __name__ == "__main__":
	main()