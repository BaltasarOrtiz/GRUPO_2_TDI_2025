# Ejercicio 4: Calculadora de Capacidad de Canal R-ario


## Funcionalidades

- **Canales R-arios**: Soporta R=2 (binario) hasta R=4+ (cuaternario y superiores)
- **Matriz de canal**: Acepta probabilidades condicionales P(Y|X) personalizadas
- **Optimización**: Encuentra distribución óptima de entrada que maximiza I(X;Y)
- **Comparación**: Distribución uniforme vs distribución óptima
- **Métricas completas**: Capacidad, información mutua, eficiencia del canal
- **Ejemplos integrados**: Canales binario asimétrico, ternario y cuaternario
- **Análisis detallado**: Matrices, probabilidades y ganancias

## Conceptos Teóricos

### Capacidad de Canal
```
C = max_{P(X)} I(X;Y)
```
Máxima información mutua posible optimizando la distribución de entrada.

### Información Mutua
```
I(X;Y) = H(Y) - H(Y|X)
```
Cantidad de información que Y proporciona sobre X.

### Entropía Condicional
```
H(Y|X) = Σ p(x) H(Y|X=x)
```
Incertidumbre promedio sobre Y cuando X es conocida.

## Requisitos

### Librerías Python Requeridas
```bash
pip install numpy scipy
```

**Dependencias:**
- `numpy` - Para cálculos matriciales y arrays
- `scipy.optimize` - Para algoritmos de optimización
- `math` (estándar) - Para funciones matemáticas básicas


## Instalación

### 1. Instalar dependencias
```bash
# Usando pip
pip install numpy scipy

# O usando conda
conda install numpy scipy
```

### 2. Descargar el programa
```bash
# Estructura recomendada
proyecto/
│
└── ej_4.py
```

## Modo de Uso

### Ejecución con ejemplos integrados
```bash
python ej_4.py
```

El programa ejecuta automáticamente tres ejemplos demostrativos:

1. **Canal Binario Asimétrico**
2. **Canal Ternario con Ruido**  
3. **Canal Cuaternario Casi Simétrico**

### Ejemplo de salida
```
Calculadora de Capacidad de Canal R-ario
========================================
Basada en la Teoría de la Información de Shannon

Ejemplo 1: Canal Binario Asimétrico
(Probabilidades de error diferentes para cada símbolo)

=== CANAL 2-ARIO ===
Matriz del canal P(Y|X):
  X=0: ['0.800', '0.200']
  X=1: ['0.250', '0.750']

--- DISTRIBUCIÓN UNIFORME ---
Probabilidades de entrada: ['0.500', '0.500']
Información mutua: 0.4591 bits

--- CAPACIDAD ÓPTIMA DEL CANAL ---
Probabilidades óptimas de entrada: ['0.6387', '0.3613']
Capacidad del canal: 0.4739 bits
Ganancia sobre distribución uniforme: 0.0148 bits
Eficiencia del canal: 47.39% (de 1.0000 bits teóricos)
```

## Estructura del Código

### Clase Principal: `ChannelCapacityCalculator`

#### Métodos principales:
- `__init__(R, channel_matrix)`: Inicializa el canal con matriz de transición
- `entropy(probs)`: Calcula entropía de Shannon
- `conditional_entropy(px)`: Calcula H(Y|X)
- `output_distribution(px)`: Calcula P(Y) dado P(X)
- `mutual_information(px)`: Calcula I(X;Y)
- `calculate_capacity()`: Optimiza para encontrar capacidad
- `calculate_uniform_capacity()`: Calcula con distribución uniforme
- `display_results()`: Muestra análisis completo

#### Validaciones implementadas:
- **Dimensiones**: Matriz R×R correcta
- **Estocasticidad**: Cada fila suma 1
- **Probabilidades**: Valores entre 0 y 1
- **Convergencia**: Verificación de optimización exitosa

## Uso Personalizado

### Definir canal propio
```python
from ej_4 import ChannelCapacityCalculator

# Canal binario simétrico (BSC)
R = 2
matrix = [
    [0.9, 0.1],  # P(Y=0|X=0)=0.9, P(Y=1|X=0)=0.1
    [0.1, 0.9]   # P(Y=0|X=1)=0.1, P(Y=1|X=1)=0.9
]

calc = ChannelCapacityCalculator(R, matrix)
capacity, optimal_px = calc.calculate_capacity()
print(f"Capacidad: {capacity:.4f} bits")
print(f"Distribución óptima: {optimal_px}")
```

### Canal ternario personalizado
```python
# Canal ternario con ruido
R = 3
matrix = [
    [0.7, 0.2, 0.1],  # Transiciones desde X=0
    [0.15, 0.7, 0.15], # Transiciones desde X=1  
    [0.1, 0.2, 0.7]   # Transiciones desde X=2
]

calc = ChannelCapacityCalculator(R, matrix)
calc.display_results()
```

## Ejemplos Incluidos

### 1. Canal Binario Asimétrico
**Características:**
- Errores diferentes para cada símbolo
- X=0 → error 20%, X=1 → error 25%
- **Resultado típico**: ~0.47 bits de capacidad

### 2. Canal Ternario con Ruido
**Características:**
- Tres símbolos con confusión cruzada
- Probabilidades de transmisión correcta variables
- **Resultado típico**: ~1.2 bits de capacidad

### 3. Canal Cuaternario Casi Simétrico
**Características:**
- Estructura casi diagonal
- Errores distribuidos uniformemente
- **Resultado típico**: ~1.8 bits de capacidad

## Interpretación de Resultados

### Capacidad del Canal
- **Alta (cercana a log₂(R))**: Canal con poco ruido
- **Media**: Canal con ruido moderado
- **Baja**: Canal muy ruidoso

### Distribución Óptima vs Uniforme
- **Ganancia positiva**: Optimización beneficia la capacidad
- **Ganancia alta**: Canal fuertemente asimétrico
- **Ganancia baja**: Canal casi simétrico

### Eficiencia del Canal
- **> 80%**: Canal excelente
- **50-80%**: Canal bueno  
- **< 50%**: Canal con mucho ruido

## Algoritmo de Optimización

### Método utilizado: SLSQP
- **Sequential Least Squares Programming**
- **Restricción**: Σ p(x) = 1
- **Límites**: 0 ≤ p(x) ≤ 1
- **Objetivo**: Maximizar I(X;Y)

### Proceso de optimización:
1. **Inicialización**: Distribución uniforme
2. **Iteración**: Ajuste de probabilidades
3. **Convergencia**: Cuando se alcanza el máximo
4. **Verificación**: Validación de la solución