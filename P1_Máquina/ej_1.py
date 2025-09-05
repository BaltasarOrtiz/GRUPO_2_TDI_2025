"""
1. Escribir un programa en lenguaje a elección, que permita:
    a. Ingresar el nombre de un archivo con extensión .wav
    b. Valide que el archivo sea con el formato adecuado.
    c. Muestre los datos de la cabecera del archivo .wav
"""

import os
import struct

def leer_cabecera_wav(nombre_archivo):
    """
    Lee y muestra la información de la cabecera de un archivo WAV.

    Args:
        nombre_archivo (str): La ruta al archivo .wav.
    """
    # 1. Validar que el archivo sea .wav y exista
    if not nombre_archivo.lower().endswith('.wav'):
        print("Error: El archivo debe tener la extensión .wav")
        return
    if not os.path.exists(nombre_archivo):
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        return

    print(f"--- Cabecera del Archivo WAV: {nombre_archivo} ---")

    # 2. Abrir el archivo en modo lectura binaria ('rb')
    with open(nombre_archivo, 'rb') as f:
        # 3. Leer los 44 bytes de la cabecera canónica
        # El formato WAV se basa en "chunks" o trozos de datos.
        # Leemos el chunk principal RIFF (primeros 12 bytes)
        chunk_id = f.read(4).decode('utf-8')
        # El formato '<i' le dice a struct que lea 4 bytes como un entero little-endian
        chunk_size = struct.unpack('<i', f.read(4))[0]
        formato = f.read(4).decode('utf-8')

        if chunk_id != 'RIFF' or formato != 'WAVE':
            print("Error: El archivo no parece ser un archivo WAVE válido.")
            return

        print(f"ID del Chunk Principal: {chunk_id}")
        print(f"Tamaño del Archivo (según cabecera): {chunk_size + 8} bytes")
        print(f"Formato: {formato}")

        # Leemos el sub-chunk 'fmt ' (24 bytes)
        subchunk1_id = f.read(4).decode('utf-8')
        subchunk1_size = struct.unpack('<i', f.read(4))[0]
        # El formato '<h' lee 2 bytes como un short integer little-endian
        audio_format = struct.unpack('<h', f.read(2))[0]
        num_canales = struct.unpack('<h', f.read(2))[0]
        sample_rate = struct.unpack('<i', f.read(4))[0]
        byte_rate = struct.unpack('<i', f.read(4))[0]
        block_align = struct.unpack('<h', f.read(2))[0]
        bits_per_sample = struct.unpack('<h', f.read(2))[0]
        
        print("\n--- Sub-chunk 'fmt ' ---")
        print(f"ID del Sub-chunk: {subchunk1_id}")
        print(f"Tamaño del Sub-chunk: {subchunk1_size}")
        print(f"Formato de Audio (1=PCM): {audio_format}")
        print(f"Número de Canales: {num_canales}")
        print(f"Frecuencia de Muestreo: {sample_rate} Hz")
        print(f"Tasa de Bytes por Segundo: {byte_rate}")
        print(f"Alineación de Bloque (Bytes por muestra): {block_align}")
        print(f"Bits por Muestra: {bits_per_sample}")

        # Leemos el inicio del sub-chunk 'data'
        subchunk2_id = f.read(4).decode('utf-8')
        subchunk2_size = struct.unpack('<i', f.read(4))[0]

        print("\n--- Sub-chunk 'data' ---")
        print(f"ID del Sub-chunk: {subchunk2_id}")
        print(f"Tamaño de los datos de audio: {subchunk2_size} bytes")
        print("-" * 40)


# --- Inicio del programa ---
if __name__ == "__main__":
    nombre = input("Ingresa el nombre del archivo .wav: ")
    leer_cabecera_wav(nombre)