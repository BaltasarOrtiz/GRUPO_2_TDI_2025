# Ejercicio 7: Algoritmo de Similitud de Cadenas Jaro-Winkler

## Problema Resuelto

### Limitaciones de la Comparación Tradicional
La comparación carácter por carácter falla con errores comunes:
- **"Juan Perez" vs "Jaun Perez"**: Intercambio de caracteres
- **"Horacio López" vs "Oracio López"**: Omisión de carácter
- **Nombres con variaciones**: Acentos, espacios, abreviaciones

### Solución: Algoritmo Jaro-Winkler
- Detecta similitud basada en caracteres comunes y transposiciones
- Da mayor peso a coincidencias en el prefijo
- Retorna valor entre 0.0 (totalmente diferentes) y 1.0 (idénticas)

## Funcionalidades

### Algoritmo Jaro Base
- Calcula coincidencias dentro de una ventana de búsqueda
- Cuenta transposiciones de caracteres coincidentes
- Fórmula: `(m/|s1| + m/|s2| + (m-t)/m) / 3`

### Mejora de Winkler
- Bonificación adicional por prefijo común
- Se aplica solo si similitud Jaro > 0.7
- Factor de escalamiento configurable (por defecto 0.1)

### Características del Algoritmo
- Tolerante a errores tipográficos comunes
- Especialmente efectivo para nombres y direcciones
- Computacionalmente eficiente
- Implementación completa desde cero

## Requisitos

### Librerías Python
**Solo librerías estándar** - No requiere instalaciones adicionales

**Python 3.x** es suficiente para ejecutar el programa.

## Instalación

1. **Descargar el archivo** `ej_7.py`
2. **Colocar en un directorio** de trabajo

```bash
# Estructura recomendada
proyecto/
│
└── ej_7.py
```

## Modo de Uso

### Ejecución básica
```bash
python ej_7.py
```

### Salida del programa
```
=== Comparación de similitud usando Jaro-Winkler ===
'Juan Perez' vs 'Jaun Perez': 0.9333
'Horacio López' vs 'Oracio López': 0.9333

Ambas cadenas muestran alta similitud a pesar de los errores tipográficos.
```

### Uso programático
```python
from ej_7 import JaroWinkler

# Crear instancia del algoritmo
comparador = JaroWinkler()

# Comparar dos cadenas
similitud = comparador.similarity("Juan Perez", "Jaun Perez")
print(f"Similitud: {similitud:.4f}")

# Ejemplo con umbral
if similitud > 0.8:
    print("Las cadenas son muy similares")
```

## Implementación Técnica

### Clase JaroWinkler

#### Parámetros configurables:
```python
threshold = 0.7     # Umbral mínimo para aplicar mejora de Winkler
three = 3           # Divisor para fórmula de Jaro (constante)
jw_coef = 0.1       # Coeficiente de escalamiento de Winkler
```

#### Métodos principales:
- `similarity(s0, s1)`: Calcula similitud Jaro-Winkler
- `matches(s0, s1)`: Encuentra coincidencias y transposiciones

### Algoritmo Paso a Paso

#### 1. Cálculo de Coincidencias
```python
# Ventana de búsqueda
ventana = max(len(cadena_larga) // 2 - 1, 0)

# Buscar coincidencias dentro de la ventana
for cada_carácter in cadena_menor:
    buscar_en_ventana(cadena_mayor, ventana)
```

#### 2. Detección de Transposiciones
```python
# Extraer secuencias de caracteres coincidentes
secuencia_s0 = [caracteres_coincidentes_s0]
secuencia_s1 = [caracteres_coincidentes_s1]

# Contar diferencias en orden
transposiciones = count(s0[i] != s1[i] for i in range(coincidencias))
```

#### 3. Fórmula de Jaro
```python
jaro = (m/len(s0) + m/len(s1) + (m-t)/m) / 3

donde:
m = número de coincidencias
t = número de transposiciones / 2
```

#### 4. Mejora de Winkler
```python
if jaro > threshold:
    prefijo = longitud_prefijo_común(s0, s1, max=4)
    jaro_winkler = jaro + (jw_coef * prefijo * (1 - jaro))
```

## Ejemplos de Casos de Uso

### Errores Tipográficos Comunes
```python
casos = [
    ("Martinez", "Martines"),      # Cambio de letra
    ("Rodriguez", "Rodríguez"),    # Acentos
    ("Ana Maria", "Ana María"),    # Acentos en nombres
    ("Garcia", "Gracia"),          # Transposición
    ("Lopez", "López"),            # Acentos simples
]

for original, variante in casos:
    sim = JaroWinkler().similarity(original, variante)
    print(f"{original} vs {variante}: {sim:.3f}")
```

### Nombres con Variaciones
```python
# Variaciones de un mismo nombre
nombre_base = "José Luis Rodríguez"
variaciones = [
    "Jose Luis Rodriguez",    # Sin acentos
    "José L. Rodríguez",     # Inicial
    "J. Luis Rodríguez",     # Nombre abreviado
    "José Luis Rodrigues",   # Variación ortográfica
]

for variacion in variaciones:
    sim = JaroWinkler().similarity(nombre_base, variacion)
    print(f"Similitud: {sim:.3f}")
```

### Detección de Duplicados
```python
def es_duplicado_probable(cadena1, cadena2, umbral=0.85):
    """
    Determina si dos cadenas probablemente representan la misma entidad.
    """
    similitud = JaroWinkler().similarity(cadena1, cadena2)
    return similitud >= umbral

# Ejemplo de uso en limpieza de datos
nombres = ["Juan Pérez", "Juan Perez", "Juan P.", "Pedro García"]
duplicados = []

for i in range(len(nombres)):
    for j in range(i+1, len(nombres)):
        if es_duplicado_probable(nombres[i], nombres[j]):
            duplicados.append((nombres[i], nombres[j]))
```

## Interpretación de Resultados

### Rangos de Similitud

#### Muy Alta (0.9 - 1.0)
- **Interpretación**: Prácticamente idénticas
- **Causa típica**: Errores tipográficos menores
- **Ejemplo**: "Juan" vs "Jaun"
- **Acción recomendada**: Considerar como duplicados

#### Alta (0.8 - 0.9)
- **Interpretación**: Muy similares
- **Causa típica**: Variaciones ortográficas
- **Ejemplo**: "Rodríguez" vs "Rodriguez"
- **Acción recomendada**: Revisar manualmente

#### Media (0.6 - 0.8)
- **Interpretación**: Algunas similitudes
- **Causa típica**: Nombres relacionados
- **Ejemplo**: "José Luis" vs "José"
- **Acción recomendada**: Considerar contexto

#### Baja (0.0 - 0.6)
- **Interpretación**: Diferentes
- **Causa típica**: Cadenas sin relación
- **Ejemplo**: "Juan" vs "Pedro"
- **Acción recomendada**: Tratarlos como distintos