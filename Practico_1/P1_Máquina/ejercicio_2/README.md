# Ejercicio 2: Analizador de Archivos BMP

## Descripción
Programa desarrollado para el **Práctico de Máquina 1** de la materia **Teoría de Información** (Licenciatura en Ciencias de la Computación, 2025).

Este analizador de archivos BMP (bitmap) permite examinar la estructura completa de imágenes en formato BMP, mostrando toda la información contenida en la cabecera de archivo y las propiedades de imagen según las especificaciones del formato bitmap de Microsoft.

## Funcionalidades

- **Validación completa**: Verifica extensión .bmp, existencia y estructura válida
- **Cabecera de archivo**: Signature, tamaño, offset de datos
- **Propiedades de imagen**: Dimensiones, profundidad de color, compresión
- **Análisis de color**: Identificación automática del tipo de color
- **Información detallada**: Resolución, paleta, colores importantes
- **Interfaz interactiva**: Análisis de múltiples archivos en una sesión
- **Validaciones adicionales**: Verificación de consistencia de datos

## Requisitos

### Librerías Python
- `struct` (estándar)
- `os` (estándar)

**No se requieren instalaciones adicionales** - Solo Python 3.x

### Archivos de prueba
- Archivos con extensión `.bmp`
- Los archivos deben estar en el mismo directorio que el script

## Instalación

1. **Clonar o descargar** el archivo `ej_2.py`
2. **Preparar archivos BMP** para análisis (colocarlos en el mismo directorio)

```bash
# Estructura de archivos recomendada
proyecto/
│
├── ej_2.py
├── imagen1.bmp
├── logo.bmp
└── foto.bmp
```

## Modo de Uso

### Ejecución básica
```bash
python ej_2.py
```

### Flujo de trabajo
1. **Iniciar el programa**
2. **Ingresar nombre del archivo** (solo el nombre, ej: `imagen.bmp`)
3. **Ver el análisis completo** de las cabeceras
4. **Decidir si analizar otro archivo** o salir con 'salir'

### Ejemplo de sesión
```
ANALIZADOR DE ARCHIVOS BMP
==============================

Ingrese el nombre del archivo BMP (o 'salir' para terminar): foto.bmp

==================================================
INFORMACIÓN DE CABECERA BMP
==================================================

--- CABECERA DE ARCHIVO (14 bytes) ---
Signature:       BM
File Size:       2,764,854 bytes
Reserved:        0
Data Offset:     54 bytes

--- CABECERA DE IMAGEN (40 bytes) ---
Size:            40 bytes
Width:           1920 píxeles
Height:          1080 píxeles
Planes:          1
Bit Count:       24 bits por píxel
Compression:     0 (Sin compresión)
Image Size:      6,220,800 bytes
X Pixels/M:      2835
Y Pixels/M:      2835
Colors Used:     0
Colors Important: 0

--- INFORMACIÓN CALCULADA ---
Tamaño real archivo: 2,764,854 bytes
Resolución:      1920 x 1080
Tipo de color:   16,777,216 colores (True Color)

Archivo analizado correctamente
--------------------------------------------------
```

## Estructura del Código

### Funciones principales:
- `leer_cabecera_bmp()`: Función principal que analiza el archivo
- `obtener_tipo_color()`: Determina el tipo de color según bits por píxel
- `main()`: Controla la interfaz interactiva

### Validaciones implementadas:
- Existencia del archivo
- Extensión .bmp (insensible a mayúsculas/minúsculas)
- Tamaño mínimo del archivo (54 bytes)
- Signature "BM" válida
- Estructura de cabeceras correcta
- Verificación de consistencia (planos, tamaño de header)

## Información Analizada

### Cabecera de Archivo (14 bytes)
| Campo | Bytes | Descripción |
|-------|-------|-------------|
| **Signature** | 2 | Siempre debe ser "BM" |
| **File Size** | 4 | Tamaño total del archivo |
| **Reserved** | 4 | Campo reservado (debe ser 0) |
| **Data Offset** | 4 | Posición donde empiezan los datos de imagen |

### Cabecera de Imagen (40 bytes)
| Campo | Bytes | Descripción |
|-------|-------|-------------|
| **Size** | 4 | Tamaño de esta cabecera (40 bytes) |
| **Width** | 4 | Ancho de la imagen en píxeles |
| **Height** | 4 | Alto de la imagen en píxeles |
| **Planes** | 2 | Número de planos (siempre 1) |
| **Bit Count** | 2 | Bits por píxel (1, 4, 8, 16, 24, 32) |
| **Compression** | 4 | Tipo de compresión (0=sin compresión) |
| **Image Size** | 4 | Tamaño de los datos de imagen |
| **X Pixels/M** | 4 | Resolución horizontal (píxeles/metro) |
| **Y Pixels/M** | 4 | Resolución vertical (píxeles/metro) |
| **Colors Used** | 4 | Número de colores en la paleta |
| **Colors Important** | 4 | Número de colores importantes |

## Tipos de Color Soportados

| Bits por píxel | Colores | Descripción |
|----------------|---------|-------------|
| **1 bit** | 2 | Monocromático (blanco y negro) |
| **4 bits** | 16 | 16 colores |
| **8 bits** | 256 | 256 colores |
| **16 bits** | 65,536 | High Color |
| **24 bits** | 16,777,216 | True Color |
| **32 bits** | 16,777,216 + alfa | True Color con transparencia |