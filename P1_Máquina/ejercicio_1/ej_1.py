#!/usr/bin/env python3
"""
Práctico de Máquina 1 - Teoría de Información
Analizador de archivos WAV (Versión Completa)
Muestra todos los datos de la cabecera WAV
"""

import struct
import os

def validar_archivo(filename):
    """Valida que el archivo tenga extensión .wav y exista"""
    if not filename.lower().endswith('.wav'):
        print(f"Error: '{filename}' no tiene extensión .wav")
        return False
    
    if not os.path.exists(filename):
        print(f"Error: El archivo '{filename}' no existe")
        return False
    
    if os.path.getsize(filename) < 44:  # Tamaño mínimo WAV
        print(f"Error: Archivo demasiado pequeño")
        return False
    
    return True

def leer_cabecera_wav(filename):
    """Lee y valida la cabecera completa de un archivo WAV"""
    try:
        with open(filename, 'rb') as f:
            # Leer cabecera RIFF (12 bytes)
            chunk_id = f.read(4)
            chunk_size = struct.unpack('<I', f.read(4))[0]
            format_type = f.read(4)
            
            # Validar RIFF WAVE
            if chunk_id != b'RIFF':
                print(f"No es archivo RIFF válido")
                return None
            
            if format_type != b'WAVE':
                print(f"No es archivo WAVE válido")
                return None
            
            # Leer subchunk fmt
            subchunk1_id = f.read(4)
            subchunk1_size = struct.unpack('<I', f.read(4))[0]
            
            if subchunk1_id != b'fmt ':
                print(f"Subchunk fmt no encontrado")
                return None
            
            # Leer datos básicos del formato (16 bytes mínimo)
            audio_format = struct.unpack('<H', f.read(2))[0]
            num_channels = struct.unpack('<H', f.read(2))[0]
            sample_rate = struct.unpack('<I', f.read(4))[0]
            byte_rate = struct.unpack('<I', f.read(4))[0]
            block_align = struct.unpack('<H', f.read(2))[0]
            bits_per_sample = struct.unpack('<H', f.read(2))[0]
            
            # Leer parámetros extra si existen
            extra_param_size = 0
            extra_params = b''
            
            if subchunk1_size > 16:
                extra_param_size = struct.unpack('<H', f.read(2))[0]
                if extra_param_size > 0:
                    extra_params = f.read(extra_param_size)
                # Saltar cualquier byte restante
                remaining = subchunk1_size - 18 - extra_param_size
                if remaining > 0:
                    f.read(remaining)
            
            # Buscar subchunk 'data'
            subchunk2_id = None
            subchunk2_size = 0
            data_sample = b''
            
            while True:
                chunk_header = f.read(8)
                if len(chunk_header) < 8:
                    print("No se encontró subchunk 'data'")
                    return None
                
                current_chunk_id = chunk_header[:4]
                current_chunk_size = struct.unpack('<I', chunk_header[4:])[0]
                
                if current_chunk_id == b'data':
                    subchunk2_id = current_chunk_id
                    subchunk2_size = current_chunk_size
                    # Leer una muestra pequeña de los datos de audio (primeros 32 bytes)
                    sample_size = min(32, current_chunk_size)
                    data_sample = f.read(sample_size)
                    break
                else:
                    # Saltar este chunk
                    f.seek(current_chunk_size, 1)
            
            # Calcular duración
            duration = subchunk2_size / byte_rate if byte_rate > 0 else 0
            
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
    """Muestra TODOS los datos de la cabecera WAV"""
    print("\n" + "="*60)
    print("DATOS COMPLETOS DEL ARCHIVO WAV")
    print("="*60)
    
    print(f"Archivo: {datos['filename']}")
    print(f"Tamaño total: {datos['file_size']:,} bytes")
    
    print(f"\n--- CABECERA RIFF ---")
    print(f"ChunkID: {datos['chunk_id']}")
    print(f"ChunkSize: {datos['chunk_size']:,} bytes")
    print(f"Format: {datos['format']}")
    
    print(f"\n--- SUBCHUNK FMT ---")
    print(f"Subchunk1ID: {datos['subchunk1_id']}")
    print(f"Subchunk1Size: {datos['subchunk1_size']} bytes")
    print(f"AudioFormat: {datos['audio_format']}")
    print(f"NumChannels: {datos['num_channels']}")
    print(f"SampleRate: {datos['sample_rate']:,} Hz")
    print(f"ByteRate: {datos['byte_rate']:,} bytes/seg")
    print(f"BlockAlign: {datos['block_align']} bytes")
    print(f"BitsPerSample: {datos['bits_per_sample']} bits")
    print(f"ExtraParamSize: {datos['extra_param_size']} bytes")
    
    if datos['extra_params']:
        # Mostrar parámetros extra en hexadecimal
        hex_params = ' '.join(f'{b:02X}' for b in datos['extra_params'])
        print(f"ExtraParams: {hex_params}")
    else:
        print(f"ExtraParams: (ninguno)")
    
    print(f"\n--- SUBCHUNK DATA ---")
    print(f"Subchunk2ID: {datos['subchunk2_id']}")
    print(f"Subchunk2Size: {datos['subchunk2_size']:,} bytes")
    print(f"Duración: {datos['duration']:.2f} segundos")
    
    # Mostrar muestra de los datos de audio
    if datos['data_sample']:
        print(f"\n--- MUESTRA DE DATA (primeros {len(datos['data_sample'])} bytes) ---")
        # Mostrar en hexadecimal
        hex_data = ' '.join(f'{b:02X}' for b in datos['data_sample'][:16])
        print(f"Data (hex): {hex_data}...")
        
        # Mostrar como valores decimales si son 16-bit samples
        if datos['bits_per_sample'] == 16 and len(datos['data_sample']) >= 4:
            sample1 = struct.unpack('<h', datos['data_sample'][0:2])[0]
            sample2 = struct.unpack('<h', datos['data_sample'][2:4])[0]
            print(f"Data (samples): {sample1}, {sample2}, ...")
    else:
        print(f"Data: (no se pudo leer muestra)")
    
    print("\n" + "="*60)
    print("ANÁLISIS COMPLETADO")
    print("="*60)

def main():
    """Función principal"""
    print("🎵 ANALIZADOR WAV COMPLETO - Práctico Máquina 1")
    print("="*50)
    base_path = os.path.dirname(os.path.abspath(__file__)) + "/"
    
    while True:
        filename = input("\n Ingrese archivo WAV (o 'salir'): ").strip()
        
        if filename.lower() in ['salir', 'exit']:
            print("¡Adios!")
            break
        
        if not filename:
            continue
        
        # Construir ruta completa
        full_path = base_path + filename
        
        # Validar archivo
        if not validar_archivo(full_path):
            continue
        
        # Leer cabecera
        datos = leer_cabecera_wav(full_path)
        
        if datos:
            mostrar_datos(datos)
        
        continuar = input("\n¿Analizar otro archivo? (s/n): ")
        if continuar.lower() not in ['s', 'si', 'y']:
            break

if __name__ == "__main__":
    main()