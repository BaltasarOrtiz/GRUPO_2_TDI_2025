# Ejercicio 8: Validador de CUIT/CUIL

## Funcionalidades

### Validación Completa
- **Verificación de formato**: XX-XXXXXXXX-X (11 dígitos + 2 guiones)
- **Validación de tipo**: Tipos válidos para CUIL y CUIT
- **Cálculo de dígito verificador**: Algoritmo oficial argentino
- **Clasificación automática**: Distingue entre CUIL y CUIT

### Tipos Soportados
- **CUIL (Personas Físicas)**: 20, 23, 24, 27
- **CUIT (Personas Jurídicas)**: 30, 33, 34

### Algoritmo de Validación
- **Base de multiplicadores**: [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
- **Suma ponderada**: Multiplica cada dígito por su factor
- **Módulo 11**: Calcula resto de división por 11
- **Casos especiales**: Manejo de restos 10 y 11

## Requisitos

### Librerías Python
**Solo librerías estándar** - No requiere instalaciones adicionales

**Python 3.x** es suficiente para ejecutar el programa.

## Instalación

1. **Descargar el archivo** `ej_8.py`
2. **Colocar en un directorio** de trabajo

```bash
# Estructura recomendada
proyecto/
│
└── ej_8.py
```

## Modo de Uso

### Ejecución interactiva
```bash
python ej_8.py
```

### Ejemplo de sesión válida
```
Ingrese un CUIT/CUIL (con guiones): 20-12345678-9
El CUIL ingresado no es válido
```

```
Ingrese un CUIT/CUIL (con guiones): 20-43926518-4
El CUIL ingresado es válido
```

### Uso programático
```python
from ej_8 import validar_cuit

# Validar un CUIT/CUIL
es_valido, tipo = validar_cuit("20-43926518-4")

if es_valido:
    print(f"El {tipo} es válido")
else:
    print(f"El {tipo} no es válido")
```

## Implementación Técnica

### Algoritmo de Validación

#### 1. Verificación de Formato
```python
# Formato esperado: XX-XXXXXXXX-X
if len(cuit) != 13 or cuit[2] != "-" or cuit[11] != "-":
    return False, "CUIT/CUIL"
```

#### 2. Validación de Tipo
```python
tipos_cuil = [20, 23, 24, 27]  # Personas físicas
tipos_cuit = [30, 33, 34]      # Personas jurídicas

tipo = int(cuit[:2])
if tipo not in tipos_validos:
    return False, "CUIT/CUIL"
```

#### 3. Cálculo del Dígito Verificador
```python
# Base de multiplicadores oficial
base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

# Extraer solo dígitos (sin guiones)
digitos = [int(i) for i in cuit if i.isdigit()]

# Suma ponderada de los primeros 10 dígitos
suma = sum(digitos[i] * base[i] for i in range(10))

# Cálculo del dígito verificador
resto = suma % 11
digito_verificador = 11 - resto

# Casos especiales
if digito_verificador == 11:
    digito_verificador = 0
if digito_verificador == 10:
    digito_verificador = 9
```

#### 4. Verificación Final
```python
# Comparar dígito calculado con el ingresado
return digito_verificador == digitos[10]
```

### Funciones Principales

#### `validar_cuit(cuit)`
- **Entrada**: String con formato XX-XXXXXXXX-X
- **Salida**: Tupla (es_válido, tipo)
- **Validaciones**: Formato, tipo, dígito verificador

#### `tipo2(tipo)`
- **Entrada**: Entero con los primeros 2 dígitos
- **Salida**: String "CUIL" o "CUIT"
- **Función**: Clasificar el tipo de documento

## Tipos de CUIT/CUIL

### CUIL - Personas Físicas

| Tipo | Descripción |
|------|-------------|
| **20** | Personas físicas masculinas |
| **23** | Personas físicas masculinas (casos especiales) |
| **24** | Personas físicas femeninas (casos especiales) |
| **27** | Personas físicas femeninas |

### CUIT - Personas Jurídicas

| Tipo | Descripción |
|------|-------------|
| **30** | Personas jurídicas |
| **33** | Personas jurídicas (casos especiales) |
| **34** | Personas jurídicas (casos especiales) |

## Ejemplos de Validación

### Casos Válidos
```python
casos_validos = [
    "20-12345678-5",    # CUIL masculino válido
    "27-98765432-1",    # CUIL femenino válido
    "30-71234567-4",    # CUIT empresa válido
    "23-45678901-3",    # CUIL especial válido
]

for caso in casos_validos:
    es_valido, tipo = validar_cuit(caso)
    print(f"{caso}: {tipo} {'válido' if es_valido else 'inválido'}")
```

### Casos Inválidos
```python
casos_invalidos = [
    "19-12345678-5",    # Tipo inválido
    "20-12345678-9",    # Dígito verificador incorrecto
    "20123456789",      # Sin guiones
    "20-1234567-89",    # Formato incorrecto
    "20-12345678-",     # Dígito verificador faltante
]
```

## Cálculo Manual del Dígito Verificador

### Ejemplo paso a paso: 20-12345678-?

```
Dígitos:    2  0  1  2  3  4  5  6  7  8
Base:       5  4  3  2  7  6  5  4  3  2
Producto:  10  0  3  4 21 24 25 24 21 16

Suma = 10 + 0 + 3 + 4 + 21 + 24 + 25 + 24 + 21 + 16 = 148
Resto = 148 % 11 = 5
Dígito verificador = 11 - 5 = 6

Por lo tanto: 20-12345678-6
```

### Casos especiales del dígito verificador:
- **Si resto = 0**: Dígito verificador = 0
- **Si resto = 1**: Dígito verificador = 0 (11-1=10 → 0)
- **Si resto = 2**: Dígito verificador = 9 (11-2=9)

## Casos de Error Manejados

### Errores de Formato
- **Longitud incorrecta**: No tiene 13 caracteres
- **Guiones faltantes**: No hay guiones en posiciones 2 y 11
- **Caracteres no numéricos**: Letras en lugar de números

### Errores de Tipo
- **Tipo inválido**: Primeros 2 dígitos no corresponden a tipos válidos
- **Combinaciones inválidas**: Tipos reservados o fuera de uso

### Errores de Validación
- **Dígito verificador incorrecto**: No coincide con el calculado
- **Cálculo fallido**: Errores en el proceso de validación
