# Ejercicio 5: Sistema de Almacenamiento de Datos de Personas

## Funcionalidades

### Almacenamiento de Longitud Fija
- Cada registro ocupa exactamente 121 bytes
- Estructura binaria con campos de tamaño predefinido
- Nombre: 50 bytes (padded con nulls)
- Dirección: 60 bytes (padded con nulls)  
- DNI: 10 bytes (padded con nulls)
- Campos S/N: 1 byte (8 bits para 8 campos booleanos)

### Almacenamiento de Longitud Variable
- Formato tipo CSV con delimitadores
- Tamaño variable según contenido real
- Campos separados por punto y coma (;)
- Codificación UTF-8
- Solo ocupa el espacio necesario

### Características Adicionales
- Generación automática de 20 registros de prueba
- Comparación automática de tamaños de archivo
- Análisis de eficiencia y ahorro de espacio
- Estructura de datos consistente entre ambos formatos

## Requisitos

### Librerías Python
- `struct` (estándar)
- `os` (estándar)

**No se requieren instalaciones adicionales** - Solo Python 3.x

## Instalación

1. **Descargar el archivo** `ej_5.py`
2. **Colocar en un directorio** de trabajo

```bash
# Estructura recomendada
proyecto/
│
└── ej_5.py
```

## Modo de Uso

### Ejecución básica
```bash
python ej_5.py
```

### Flujo automático
El programa ejecuta automáticamente:
1. **Generación de datos**: 20 registros de ejemplo
2. **Almacenamiento fijo**: Guarda en `fijos.dat`
3. **Almacenamiento variable**: Guarda en `variable.dat`
4. **Comparación**: Muestra diferencias de tamaño

### Ejemplo de salida
```
Generando 20 registros de ejemplo...
Guardando datos en archivo de longitud fija...
Guardando datos en archivo de longitud variable...

==================================================
     COMPARACIÓN DE TAMAÑOS DE ARCHIVO
==================================================
Archivo de longitud fija ('fijos.dat'):      2,420 bytes
Archivo de longitud variable ('variable.dat'): 1,180 bytes
--------------------------------------------------
El archivo de longitud variable es 1,240 bytes más pequeño.
Esto representa un ahorro del 51.2% en espacio de almacenamiento.
Demuestra la eficiencia en espacio de los registros de longitud variable.
==================================================
Registros procesados: 20
Bytes por registro (fijo): 121
Bytes promedio por registro (variable): 59
```

## Estructura de Datos

### Campos almacenados por persona:
1. **Nombre**: Apellido y nombre completo
2. **Dirección**: Dirección de residencia
3. **DNI**: Documento Nacional de Identidad
4. **8 Campos S/N**: Campos bivaluados True/False

### Campos S/N incluidos:
- Estudios primarios (S/N)
- Estudios secundarios (S/N)
- Estudios universitarios (S/N)
- Vivienda propia (S/N)
- Obra social (S/N)
- Campo adicional 1 (S/N)
- Campo adicional 2 (S/N)
- Campo adicional 3 (S/N)

## Implementación Técnica

### Clase Persona
```python
class Persona:
    def __init__(self, nombre, direccion, dni, estudios, vivienda, etc):
        self.nombre = nombre
        self.direccion = direccion
        self.dni = dni
        self.campos_sn = estudios + vivienda + etc  # 8 campos booleanos
```

### Longitud Fija - Formato Binario
- **Formato struct**: `'50s 60s 10s B'`
- **Empaquetado de booleanos**: 8 campos en 1 byte usando operaciones de bits
- **Padding automático**: Completa con nulls hasta tamaño fijo
- **Total por registro**: 121 bytes exactos

### Longitud Variable - Formato CSV
- **Delimitador**: Punto y coma (;)
- **Codificación**: UTF-8
- **Formato**: `Nombre;Dirección;DNI;S;N;S;N;S;N;S;N`
- **Tamaño**: Variable según contenido

## Análisis de Eficiencia

### Ventajas Longitud Fija
- **Acceso directo**: Cálculo directo de posición de registro
- **Velocidad de búsqueda**: O(1) para acceso por índice
- **Simplicidad**: Estructura predecible
- **Alineación**: Optimizada para sistemas binarios

### Ventajas Longitud Variable
- **Eficiencia de espacio**: Solo usa espacio necesario
- **Flexibilidad**: Campos pueden crecer sin reestructurar
- **Legibilidad**: Formato texto más fácil de interpretar
- **Portabilidad**: CSV es un estándar universal

### Casos típicos de ahorro:
- **Nombres cortos**: Gran ahorro en campos de texto
- **Datos simples**: Menos overhead por registro
- **Archivos grandes**: El ahorro se multiplica por número de registros

## Generación de Datos de Prueba

### Patrones implementados:
```python
# Datos base variables
nombre = f"Apellido{i} Nombre{i}"
direccion = f"Calle Falsa {i*10}, Ciudad"
dni = f"30{i:06d}"

# Patrones para campos S/N
estudios_primarios = True                    # Siempre True
estudios_secundarios = i % 2 == 0           # Números pares
estudios_universitarios = i % 5 == 0        # Múltiplos de 5
vivienda_propia = i % 3 == 0               # Múltiplos de 3
obra_social = True                          # Siempre True
otros_campos = [False, True, i > 10]        # Patrones mixtos
```

## Archivos Generados

### fijos.dat
- **Formato**: Binario
- **Estructura**: Registros de 121 bytes
- **Acceso**: Directo por posición
- **Contenido**: Datos empaquetados con struct

### variable.dat
- **Formato**: Texto CSV
- **Estructura**: Una línea por registro
- **Acceso**: Secuencial línea por línea
- **Contenido**: Campos separados por ";"

## Interpretación de Resultados

### Ahorro Significativo (> 40%)
- **Causa**: Nombres y direcciones cortos vs espacios fijos
- **Beneficio**: Muy eficiente para datos de tamaño variable
- **Uso recomendado**: Sistemas con restricciones de almacenamiento

### Ahorro Moderado (20-40%)
- **Causa**: Balance entre overhead y ahorro real
- **Beneficio**: Buena eficiencia general
- **Uso recomendado**: Mayoría de aplicaciones

### Sin Ahorro (< 10%)
- **Causa**: Overhead de delimitadores supera ahorro
- **Situación**: Datos muy uniformes o pocos registros
- **Consideración**: Evaluar beneficios de acceso directo