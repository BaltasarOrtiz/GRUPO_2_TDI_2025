"""
Práctico de Máquina 1 - Teoría de Información
Analizador de archivos WAV (Versión Completa)
Muestra todos los datos de la cabecera WAV

Este programa lee y analiza la estructura completa de archivos WAV,
incluyendo la cabecera RIFF, el subchunk fmt y el subchunk data.
"""

import struct
import os

def validar_archivo(filename):
	"""
	Valida que el archivo tenga extensión .wav y exista
	
	Args:
		filename (str): Ruta del archivo a validar
		
	Returns:
		bool: True si el archivo es válido, False en caso contrario
	"""
	# Verificar extensión .wav (insensible a mayúsculas/minúsculas)
	if not filename.lower().endswith('.wav'):
		print(f"Error: '{filename}' no tiene extensión .wav")
		return False
	
	# Verificar que el archivo existe
	if not os.path.exists(filename):
		print(f"Error: El archivo '{filename}' no existe")
		return False
	
	# Verificar tamaño mínimo (44 bytes es el mínimo para una cabecera WAV válida)
	if os.path.getsize(filename) < 44:
		print(f"Error: Archivo demasiado pequeño")
		return False
	
	return True

def leer_cabecera_wav(filename):
	"""
	Lee y valida la cabecera completa de un archivo WAV
	
	Args:
		filename (str): Ruta del archivo WAV a analizar
		
	Returns:
		dict: Diccionario con todos los datos de la cabecera WAV, o None si hay error
	"""
	try:
		with open(filename, 'rb') as f:
			# =================== CABECERA RIFF (12 bytes) ===================
			# Los primeros 4 bytes deben ser 'RIFF'
			chunk_id = f.read(4)
			# Los siguientes 4 bytes indican el tamaño del archivo - 8 bytes
			chunk_size = struct.unpack('<I', f.read(4))[0]  # Little-endian unsigned int
			# Los siguientes 4 bytes deben ser 'WAVE'
			format_type = f.read(4)
			
			# Validar que es un archivo RIFF válido
			if chunk_id != b'RIFF':
				print(f"No es archivo RIFF válido")
				return None
			
			# Validar que es un archivo WAVE válido
			if format_type != b'WAVE':
				print(f"No es archivo WAVE válido")
				return None
			
			# =================== SUBCHUNK FMT ===================
			# Los siguientes 4 bytes deben ser 'fmt ' (con espacio)
			subchunk1_id = f.read(4)
			# Tamaño del subchunk fmt (usualmente 16, pero puede ser mayor)
			subchunk1_size = struct.unpack('<I', f.read(4))[0]
			
			if subchunk1_id != b'fmt ':
				print(f"Subchunk fmt no encontrado")
				return None
			
			# ========== DATOS BÁSICOS DEL FORMATO (16 bytes mínimo) ==========
			# Formato de audio (1 = PCM, otros valores indican compresión)
			audio_format = struct.unpack('<H', f.read(2))[0]  # Unsigned short
			# Número de canales (1 = mono, 2 = estéreo)
			num_channels = struct.unpack('<H', f.read(2))[0]
			# Frecuencia de muestreo en Hz (ej: 44100)
			sample_rate = struct.unpack('<I', f.read(4))[0]
			# Bytes por segundo (SampleRate * NumChannels * BitsPerSample/8)
			byte_rate = struct.unpack('<I', f.read(4))[0]
			# Bytes por muestra incluyendo todos los canales
			block_align = struct.unpack('<H', f.read(2))[0]
			# Bits por muestra (8, 16, 24, 32)
			bits_per_sample = struct.unpack('<H', f.read(2))[0]
			
			# ========== PARÁMETROS EXTRA (si existen) ==========
			extra_param_size = 0
			extra_params = b''
			
			# Si el subchunk fmt es mayor a 16 bytes, hay parámetros extra
			if subchunk1_size > 16:
				# Tamaño de los parámetros extra
				extra_param_size = struct.unpack('<H', f.read(2))[0]
				# Leer parámetros extra si existen
				if extra_param_size > 0:
					extra_params = f.read(extra_param_size)
				# Saltar cualquier byte restante del subchunk fmt
				remaining = subchunk1_size - 18 - extra_param_size
				if remaining > 0:
					f.read(remaining)
			
			# =================== BUSCAR SUBCHUNK 'DATA' ===================
			# Puede haber otros chunks antes del data (ej: LIST, INFO)
			subchunk2_id = None
			subchunk2_size = 0
			data_sample = b''
			
			# Buscar el chunk 'data' iterando por todos los chunks
			while True:
				# Leer cabecera del chunk (8 bytes: 4 ID + 4 tamaño)
				chunk_header = f.read(8)
				if len(chunk_header) < 8:
					print("No se encontró subchunk 'data'")
					return None
				
				# Extraer ID y tamaño del chunk actual
				current_chunk_id = chunk_header[:4]
				current_chunk_size = struct.unpack('<I', chunk_header[4:])[0]
				
				# Si encontramos el chunk 'data', procesarlo
				if current_chunk_id == b'data':
					subchunk2_id = current_chunk_id
					subchunk2_size = current_chunk_size
					# Leer una muestra pequeña de los datos de audio (máximo 32 bytes)
					sample_size = min(32, current_chunk_size)
					data_sample = f.read(sample_size)
					break
				else:
					# Si no es 'data', saltar este chunk completo
					f.seek(current_chunk_size, 1)  # Seek relativo
			
			# =================== CALCULAR DURACIÓN ===================
			# Duración en segundos = bytes de audio / bytes por segundo
			duration = subchunk2_size / byte_rate if byte_rate > 0 else 0
			
			# Retornar diccionario con todos los datos extraídos
			return {
				'filename': filename,
				'file_size': os.path.getsize(filename),
				'chunk_id': chunk_id.decode('ascii'),
				'chunk_size': chunk_size,
				'format': format_type.decode('ascii'),
				'subchunk1_id': subchunk1_id.decode('ascii').strip(),
				'subchunk1_size': subchunk1_size,
				'audio_format': audio_format,
				'num_channels': num_channels,
				'sample_rate': sample_rate,
				'byte_rate': byte_rate,
				'block_align': block_align,
				'bits_per_sample': bits_per_sample,
				'extra_param_size': extra_param_size,
				'extra_params': extra_params,
				'subchunk2_id': subchunk2_id.decode('ascii') if subchunk2_id else 'N/A',
				'subchunk2_size': subchunk2_size,
				'data_sample': data_sample,
				'duration': duration
			}
			
	except Exception as e:
		print(f"Error al leer archivo: {e}")
		return None

def mostrar_datos(datos):
	"""
	Muestra TODOS los datos de la cabecera WAV en formato organizado
	
	Args:
		datos (dict): Diccionario con los datos extraídos del archivo WAV
	"""
	print("\n" + "="*60)
	print("DATOS COMPLETOS DEL ARCHIVO WAV")
	print("="*60)
	
	# =================== INFORMACIÓN GENERAL ===================
	print(f"Archivo: {datos['filename']}")
	print(f"Tamaño total: {datos['file_size']:,} bytes")
	
	# =================== CABECERA RIFF ===================
	print(f"\n--- CABECERA RIFF ---")
	print(f"ChunkID: {datos['chunk_id']}")          # Debe ser 'RIFF'
	print(f"ChunkSize: {datos['chunk_size']:,} bytes")  # Tamaño archivo - 8
	print(f"Format: {datos['format']}")             # Debe ser 'WAVE'
	
	# =================== SUBCHUNK FMT ===================
	print(f"\n--- SUBCHUNK FMT ---")
	print(f"Subchunk1ID: {datos['subchunk1_id']}")     # Debe ser 'fmt '
	print(f"Subchunk1Size: {datos['subchunk1_size']} bytes")  # Tamaño del fmt chunk
	print(f"AudioFormat: {datos['audio_format']}")     # 1=PCM, otros=compresión
	print(f"NumChannels: {datos['num_channels']}")     # 1=mono, 2=estéreo
	print(f"SampleRate: {datos['sample_rate']:,} Hz")  # Frecuencia muestreo
	print(f"ByteRate: {datos['byte_rate']:,} bytes/seg")  # Bytes por segundo
	print(f"BlockAlign: {datos['block_align']} bytes") # Bytes por frame
	print(f"BitsPerSample: {datos['bits_per_sample']} bits")  # Resolución
	print(f"ExtraParamSize: {datos['extra_param_size']} bytes")  # Parámetros extra
	
	# Mostrar parámetros extra si existen
	if datos['extra_params']:
		# Convertir bytes a representación hexadecimal
		hex_params = ' '.join(f'{b:02X}' for b in datos['extra_params'])
		print(f"ExtraParams: {hex_params}")
	else:
		print(f"ExtraParams: (ninguno)")
	
	# =================== SUBCHUNK DATA ===================
	print(f"\n--- SUBCHUNK DATA ---")
	print(f"Subchunk2ID: {datos['subchunk2_id']}")     # Debe ser 'data'
	print(f"Subchunk2Size: {datos['subchunk2_size']:,} bytes")  # Bytes de audio
	print(f"Duración: {datos['duration']:.2f} segundos")        # Duración calculada
	
	# =================== MUESTRA DE DATOS DE AUDIO ===================
	if datos['data_sample']:
		print(f"\n--- MUESTRA DE DATA (primeros {len(datos['data_sample'])} bytes) ---")
		
		# Mostrar en formato hexadecimal (más legible para datos binarios)
		hex_data = ' '.join(f'{b:02X}' for b in datos['data_sample'][:16])
		print(f"Data (hex): {hex_data}...")
		
		# Si es audio de 16 bits, mostrar algunas muestras como valores decimales
		if datos['bits_per_sample'] == 16 and len(datos['data_sample']) >= 4:
			# Interpretar como signed short (16-bit) little-endian
			sample1 = struct.unpack('<h', datos['data_sample'][0:2])[0]
			sample2 = struct.unpack('<h', datos['data_sample'][2:4])[0]
			print(f"Data (samples): {sample1}, {sample2}, ...")
	else:
		print(f"Data: (no se pudo leer muestra)")
	
	print("\n" + "="*60)
	print("ANÁLISIS COMPLETADO")
	print("="*60)

def main():
	"""
	Función principal del programa
	Maneja la interfaz de usuario y el flujo principal del programa
	"""
	print("🎵 ANALIZADOR WAV COMPLETO - Práctico Máquina 1")
	print("="*50)
	
	# Obtener directorio base donde está el script
	base_path = os.path.dirname(os.path.abspath(__file__)) + "/"
	
	# Bucle principal del programa
	while True:
		# Solicitar nombre del archivo al usuario
		filename = input("\n Ingrese archivo WAV (o 'salir'): ").strip()
		
		# Verificar si el usuario quiere salir
		if filename.lower() in ['salir', 'exit']:
			print("¡Adios!")
			break
		
		# Ignorar entradas vacías
		if not filename:
			continue
		
		# Construir ruta completa del archivo
		full_path = base_path + filename
		
		# Validar que el archivo es válido
		if not validar_archivo(full_path):
			continue  # Volver a pedir archivo si no es válido
		
		# Leer y analizar la cabecera WAV
		datos = leer_cabecera_wav(full_path)
		
		# Si se pudieron extraer los datos, mostrarlos
		if datos:
			mostrar_datos(datos)
		
		# Preguntar si quiere analizar otro archivo
		continuar = input("\n¿Analizar otro archivo? (s/n): ")
		if continuar.lower() not in ['s', 'si', 'y']:
			break

# Punto de entrada del programa
if __name__ == "__main__":
	main()