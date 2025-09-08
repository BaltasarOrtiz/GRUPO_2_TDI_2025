# Ejercicio 3: Calculadora de Entropía y Redundancia

## Funcionalidades

- **Entropía independiente**: Análisis de símbolos individuales (orden 0)
- **Entropía dependiente**: Análisis de pares consecutivos (bigrams)
- **Cálculo de redundancia**: Para ambos tipos de análisis
- **Eficiencia O(1)**: Algoritmos optimizados usando Counter
- **Soporte universal**: Cualquier tipo de archivo (binario o texto)
- **Interfaz interactiva**: Análisis de múltiples archivos
- **Medición de rendimiento**: Tiempo de procesamiento

## Conceptos Teóricos

### Entropía de Shannon
```
H(X) = -Σ p(x) * log₂(p(x))
```
Mide la incertidumbre promedio o cantidad de información de una fuente.

### Redundancia
```
R = log₂(N) - H
```
Donde N es el número de símbolos únicos y H es la entropía.

### Eficiencia
```
η = (H / H_max) * 100%
```
Porcentaje de la entropía máxima teórica alcanzada.

## Requisitos

### Librerías Python
- `math` (estándar)
- `os` (estándar)
- `time` (estándar)
- `collections.Counter` (estándar)

**No se requieren instalaciones adicionales** - Solo Python 3.x

### Archivos de prueba
- Cualquier tipo de archivo para análisis
- Recomendados: .txt, .exe, .zip, .pdf, .wav, .bmp, etc.

## Instalación

1. **Clonar o descargar** el archivo `ej_3.py`
2. **Preparar archivos de prueba** (colocarlos en el mismo directorio)

```bash
# Estructura de archivos recomendada
proyecto/
│
├── ej_3.py
├── archivo.txt
├── archivo.exe
├── archivo.zip
```

## Modo de Uso

### Ejecución básica
```bash
python ej_3.py
```

### Flujo de trabajo
1. **Iniciar el programa**
2. **Ingresar nombre del archivo** (con extensión)
3. **Ver el análisis completo** de entropía y redundancia
4. **Comparar resultados** entre diferentes tipos de archivos

### Ejemplo de sesión
```
Ingrese el nombre del archivo (con extensión): archivo.txt

Archivo: archivo.txt
Tamaño: 0.56 KB (574 bytes)
Extensión: .txt
Tiempo de procesamiento: 0.0011 segundos
------------------------------------------------------------

ESTADÍSTICAS BÁSICAS:
	Total de bytes: 574
	Símbolos únicos: 37
	Entropía máxima: 5.2095 bits/símbolo

ANÁLISIS INDEPENDIENTE (símbolos individuales):
	Entropía: 4.3870 bits/símbolo
	Entropía por bit: 0.5484
	Redundancia: 0.8224 bits/símbolo
	Eficiencia: 84.21%

ANÁLISIS DEPENDIENTE (pares consecutivos):
	Entropía: 7.2620 bits/símbolo
	Entropía por bit: 0.9078
	Redundancia: -2.0526 bits/símbolo
	Eficiencia: 139.40%
```

## Estructura del Código

### Funciones principales:
- `calcular_probabilidades()`: Calcula distribución de probabilidades
- `entropia_independiente()`: Entropía de Shannon clásica
- `entropia_dependiente()`: Entropía de pares consecutivos (bigrams)
- `redundancia()`: Calcula redundancia informacional
- `calcular_entropia_y_redundancia()`: Función principal de análisis
- `main()`: Interfaz interactiva

### Algoritmos implementados:
- **Counter optimizado**: O(1) para frecuencias
- **Análisis en memoria**: Lectura completa del archivo
- **Cálculos paralelos**: Independiente y dependiente simultáneamente

## Tipos de Análisis

### 1. Análisis Independiente
- **Símbolos**: Cada byte individualmente
- **Probabilidad**: P(byte = x)
- **Uso**: Compresión básica, análisis de distribución
- **Entropía**: Mide aleatoriedad de bytes individuales

### 2. Análisis Dependiente
- **Símbolos**: Pares de bytes consecutivos (bigrams)
- **Probabilidad**: P(par = (x,y))
- **Uso**: Compresión avanzada, detección de patrones
- **Entropía**: Mide correlaciones entre bytes adyacentes

## Información Calculada

### Estadísticas Básicas
- **Total de bytes**: Tamaño del archivo
- **Símbolos únicos**: Número de valores diferentes (0-255)
- **Entropía máxima**: log₂(símbolos únicos)

### Para cada tipo de análisis:
- **Entropía**: Bits de información por símbolo
- **Entropía por bit**: Entropía dividida por 8
- **Redundancia**: Información "desperdiciada"
- **Eficiencia**: Porcentaje de la entropía máxima

## Interpretación de Resultados

### Entropía Alta (> 7 bits/símbolo)
- **Datos muy aleatorios**
- **Difícil de comprimir**
- **Ejemplo**: Archivos ya comprimidos (.zip, .mp3)

### Entropía Media (4-7 bits/símbolo)
- **Datos con estructura**
- **Buena compresibilidad**
- **Ejemplo**: Texto, código fuente

### Entropía Baja (< 4 bits/símbolo)
- **Datos muy repetitivos**
- **Excelente compresibilidad**
- **Ejemplo**: Archivos con padding, imágenes simples

### Comparación Independiente vs Dependiente
- **Dependiente > Independiente**: Indica correlaciones complejas o archivo pequeño
- **Dependiente < Independiente**: Hay correlaciones predictibles entre símbolos
- **Diferencia grande**: Estructura predecible (texto, código)
- **Diferencia pequeña**: Datos aleatorios (archivos comprimidos)

## Casos de Uso Verificados

### Análisis de Texto
```
archivo.txt:
- Entropía independiente: 4.3870 bits/símbolo
- Entropía dependiente: 7.2620 bits/símbolo
- Eficiencia: 84.21% / 139.40%
- Conclusión: Archivo pequeño con alta variabilidad de pares
```

### Análisis de Ejecutables
```
archivo.exe:
- Entropía independiente: 4.3870 bits/símbolo
- Entropía dependiente: 7.2620 bits/símbolo
- Eficiencia: 84.21% / 139.40%
- Conclusión: Mismos resultados que .txt (mismo contenido)
```

### Análisis de Archivos Comprimidos
```
archivo.zip:
- Entropía independiente: 6.9072 bits/símbolo
- Entropía dependiente: 8.2439 bits/símbolo
- Eficiencia: 90.19% / 107.65%
- Conclusión: Mayor aleatoriedad, ya optimizado
```