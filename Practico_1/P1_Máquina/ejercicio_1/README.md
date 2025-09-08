# Ejercicio 1: Analizador de Archivos WAV

## Funcionalidades

- **Validación de archivos**: Verifica extensión .wav, existencia y tamaño mínimo
- **Análisis de cabecera RIFF**: Muestra ChunkID, ChunkSize y Format
- **Información del formato**: AudioFormat, canales, frecuencia de muestreo, bits por muestra
- **Datos de audio**: Tamaño de datos, duración calculada y muestra de los primeros bytes
- **Interfaz interactiva**: Permite analizar múltiples archivos en una sesión
- **Reporte completo**: Todos los campos de la cabecera WAV de forma organizada

## Requisitos

### Librerías Python
- `struct` (estándar)
- `os` (estándar)

**No se requieren instalaciones adicionales** - Solo Python 3.x

### Archivos de prueba
- Archivos con extensión `.wav`
- Los archivos deben estar en el mismo directorio que el script

## Instalación

1. **Clonar o descargar** el archivo `ej_1.py`
2. **Preparar archivos WAV** para análisis (colocarlos en el mismo directorio)

```bash
# Estructura de archivos recomendada
proyecto/
│
├── ej_1.py
├── audio1.wav
├── audio2.wav
└── musica.wav
```

## Modo de Uso

### Ejecución básica
```bash
python ej_1.py
```

### Flujo de trabajo
1. **Iniciar el programa**
2. **Ingresar nombre del archivo** (solo el nombre, ej: `audio.wav`)
3. **Ver el análisis completo** de la cabecera
4. **Decidir si analizar otro archivo** o salir

### Ejemplo de sesión
```
ANALIZADOR WAV COMPLETO - Práctico Máquina 1
==================================================

 Ingrese archivo WAV (o 'salir'): musica.wav

============================================================
DATOS COMPLETOS DEL ARCHIVO WAV
============================================================
Archivo: musica.wav
Tamaño total: 5,234,567 bytes

--- CABECERA RIFF ---
ChunkID: RIFF
ChunkSize: 5,234,559 bytes
Format: WAVE

--- SUBCHUNK FMT ---
Subchunk1ID: fmt 
Subchunk1Size: 16 bytes
AudioFormat: 1
NumChannels: 2
SampleRate: 44,100 Hz
ByteRate: 176,400 bytes/seg
BlockAlign: 4 bytes
BitsPerSample: 16 bits
ExtraParamSize: 0 bytes
ExtraParams: (ninguno)

--- SUBCHUNK DATA ---
Subchunk2ID: data
Subchunk2Size: 5,234,523 bytes
Duración: 29.67 segundos

--- MUESTRA DE DATA (primeros 16 bytes) ---
Data (hex): A1 B2 C3 D4 E5 F6 07 18...
Data (samples): -24159, 17364, ...

============================================================
ANÁLISIS COMPLETADO
============================================================

¿Analizar otro archivo? (s/n): n
```

## Estructura del Código

### Funciones principales:
- `validar_archivo()`: Validaciones previas al análisis
- `leer_cabecera_wav()`: Extrae toda la información de las cabeceras
- `mostrar_datos()`: Presenta los resultados de forma organizada
- `main()`: Controla la interfaz interactiva

### Validaciones implementadas:
- Extensión .wav (insensible a mayúsculas/minúsculas)
- Existencia del archivo
- Tamaño mínimo de 44 bytes
- Signature RIFF válida
- Formato WAVE válido
- Presencia del subchunk 'fmt '
- Búsqueda del subchunk 'data'

## Información Mostrada

### Cabecera RIFF (12 bytes)
- **ChunkID**: Identificador "RIFF"
- **ChunkSize**: Tamaño total del archivo - 8 bytes
- **Format**: Debe ser "WAVE"

### Subchunk fmt (16+ bytes)
- **AudioFormat**: 1=PCM, otros=compresión
- **NumChannels**: 1=mono, 2=estéreo
- **SampleRate**: Frecuencia de muestreo (Hz)
- **ByteRate**: Bytes por segundo
- **BlockAlign**: Bytes por frame
- **BitsPerSample**: Resolución (8, 16, 24, 32 bits)

### Subchunk data
- **Tamaño de datos**: Bytes de audio puro
- **Duración**: Calculada automáticamente
- **Muestra de datos**: Primeros bytes en hex y decimal
