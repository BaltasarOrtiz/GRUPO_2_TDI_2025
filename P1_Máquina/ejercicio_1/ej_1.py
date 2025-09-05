#!/usr/bin/env python3
"""
Práctico de Máquina 1 - Teoría de Información
Analizador de archivos WAV (Versión Simplificada)
"""

import struct
import os

base_path = os.path.dirname(os.path.abspath(__file__)) + "/"

def validar_archivo(filename):
    """Valida que el archivo tenga extensión .wav y exista"""
    if not filename.lower().endswith('.wav'):
        print(f"❌ Error: '{filename}' no tiene extensión .wav")
        return False
    
    if not os.path.exists(filename):
        print(f"❌ Error: El archivo '{filename}' no existe")
        return False
    
    """ if os.path.getsize(filename) < 44:  # Tamaño mínimo WAV
        print(f"❌ Error: Archivo demasiado pequeño")
        return False """
    
    return True

def leer_cabecera_wav(filename):
    """Lee y valida la cabecera de un archivo WAV"""
    try:
        with open(filename, 'rb') as f:
            # Leer cabecera RIFF (12 bytes)
            chunk_id = f.read(4)
            chunk_size = struct.unpack('<I', f.read(4))[0]
            format_type = f.read(4)
            
            # Validar RIFF WAVE
            if chunk_id != b'RIFF':
                print(f"❌ No es archivo RIFF válido")
                return None
            
            if format_type != b'WAVE':
                print(f"❌ No es archivo WAVE válido")
                return None
            
            # Leer subchunk fmt
            subchunk1_id = f.read(4)
            subchunk1_size = struct.unpack('<I', f.read(4))[0]
            
            if subchunk1_id != b'fmt ':
                print(f"❌ Subchunk fmt no encontrado")
                return None
            
            # Leer datos del formato
            audio_format = struct.unpack('<H', f.read(2))[0]
            num_channels = struct.unpack('<H', f.read(2))[0]
            sample_rate = struct.unpack('<I', f.read(4))[0]
            byte_rate = struct.unpack('<I', f.read(4))[0]
            block_align = struct.unpack('<H', f.read(2))[0]
            bits_per_sample = struct.unpack('<H', f.read(2))[0]
            
            # Saltar parámetros extra si existen
            if subchunk1_size > 16:
                f.read(subchunk1_size - 16)
            
            # Buscar subchunk 'data'
            while True:
                chunk_header = f.read(8)
                if len(chunk_header) < 8:
                    print("❌ No se encontró subchunk 'data'")
                    return None
                
                subchunk2_id = chunk_header[:4]
                subchunk2_size = struct.unpack('<I', chunk_header[4:])[0]
                
                if subchunk2_id == b'data':
                    break
                else:
                    f.seek(subchunk2_size, 1)  # Saltar chunk
            
            # Calcular duración
            duration = subchunk2_size / byte_rate if byte_rate > 0 else 0
            
            return {
                'filename': filename,
                'file_size': os.path.getsize(filename),
                'chunk_id': chunk_id.decode('ascii'),
                'chunk_size': chunk_size,
                'format_type': format_type.decode('ascii'),
                'subchunk1_size': subchunk1_size,
                'audio_format': audio_format,
                'num_channels': num_channels,
                'sample_rate': sample_rate,
                'byte_rate': byte_rate,
                'block_align': block_align,
                'bits_per_sample': bits_per_sample,
                'subchunk2_size': subchunk2_size,
                'duration': duration
            }
            
    except Exception as e:
        print(f"❌ Error al leer archivo: {e}")
        return None

def mostrar_datos(datos):
    """Muestra los datos de la cabecera"""
    print("\n" + "="*50)
    print("📄 DATOS DEL ARCHIVO WAV")
    print("="*50)
    
    print(f"Archivo: {datos['filename']}")
    print(f"Tamaño: {datos['file_size']:,} bytes")
    
    print(f"\n--- CABECERA RIFF ---")
    print(f"ChunkID: {datos['chunk_id']}")
    print(f"ChunkSize: {datos['chunk_size']:,} bytes")
    print(f"Format: {datos['format_type']}")
    
    print(f"\n--- SUBCHUNK FMT ---")
    print(f"Subchunk1Size: {datos['subchunk1_size']} bytes")
    print(f"AudioFormat: {datos['audio_format']}")
    print(f"NumChannels: {datos['num_channels']}")
    print(f"SampleRate: {datos['sample_rate']:,} Hz")
    print(f"ByteRate: {datos['byte_rate']:,} bytes/seg")
    print(f"BlockAlign: {datos['block_align']} bytes")
    print(f"BitsPerSample: {datos['bits_per_sample']} bits")
    
    print(f"\n--- SUBCHUNK DATA ---")
    print(f"Subchunk2Size: {datos['subchunk2_size']:,} bytes")
    print(f"Duración: {datos['duration']:.2f} segundos")
    
    print("="*50)
    print("✅ ANÁLISIS COMPLETADO")

def main():
    """Función principal"""
    print("🎵 ANALIZADOR WAV - Práctico Máquina 1")
    print("="*40)
    
    while True:
        filename = base_path + input("\n📁 Ingrese archivo WAV (o 'salir'): ").strip()
        
        if filename.lower() in ['salir', 'exit']:
            print("👋 ¡Hasta luego!")
            break
        
        if not filename:
            continue
        
        # Validar archivo
        if not validar_archivo(filename):
            continue
        
        # Leer cabecera
        datos = leer_cabecera_wav(filename)
        
        if datos:
            mostrar_datos(datos)
        
        continuar = input("\n¿Analizar otro archivo? (s/n): ")
        if continuar.lower() not in ['s', 'si', 'y']:
            break

if __name__ == "__main__":
    main()