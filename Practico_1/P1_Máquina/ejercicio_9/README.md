# Ejercicio 9: Sistema Cliente-Servidor con Compresión

## Funcionalidades

### Sistema de Comunicación
- **Protocolo TCP**: Comunicación confiable entre procesos
- **Arquitectura cliente-servidor**: Servidor acepta conexiones de clientes
- **Compresión automática**: Todos los datos se comprimen antes del envío
- **Descompresión transparente**: El receptor obtiene datos descomprimidos

### Módulo de Compresión
- **Alfabeto reducido**: Solo caracteres A, B, C, D, E, F, G, H
- **Compresión 3:8**: Cada carácter usa 3 bits en lugar de 8 bits ASCII
- **Eficiencia**: Reducción teórica del 62.5% en tamaño
- **Formato binario**: Empaquetado optimizado en bytes

### Características de Implementación
- **Threading**: Servidor y cliente ejecutan simultáneamente
- **Clase base común**: Funcionalidad compartida entre cliente y servidor
- **Manejo de errores**: Gestión de conexiones y excepciones
- **Demostración integrada**: Ejemplo funcional incluido

## Requisitos

### Librerías Python
- `socket` (estándar)
- `threading` (estándar)

### Archivos Requeridos
- `ej_9.py` (programa principal)
- `Compresor.py` (módulo de compresión)

**No se requieren instalaciones adicionales** - Solo Python 3.x

## Instalación

1. **Descargar ambos archivos** en el mismo directorio
2. **Verificar estructura** de archivos

```bash
# Estructura requerida
proyecto/
│
├── ej_9.py          # Programa principal con cliente/servidor
└── Compresor.py     # Módulo de compresión personalizado
```

## Modo de Uso

### Ejecución de la demostración
```bash
python ej_9.py
```

### Salida esperada
```
ABCDE
AAAABDAEB
```

**Explicación del flujo:**
1. **Servidor inicia** y espera conexiones en localhost:27015
2. **Cliente se conecta** al servidor
3. **Cliente envía** "BDAEB" (comprimido automáticamente)
4. **Servidor recibe** y descomprime "BDAEB"
5. **Servidor responde** con "ABCDE" (comprimido)
6. **Servidor responde** con "AAAA" + "BDAEB" (comprimido)
7. **Cliente recibe** ambas respuestas (descomprimidas automáticamente)

## Estructura del Código

### Clase Base: `__Base`
```python
class __Base:
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def send(self, string):
        # Comprime automáticamente antes de enviar
        self._socket.send(Compresor.compress(string))
    
    def receive(self):
        # Descomprime automáticamente al recibir
        return Compresor.decompress(self._socket.recv(1024))
```

### Clase Cliente: `Client`
```python
class Client(__Base):
    def __init__(self, ip='localhost', port=27015):
        super().__init__()
        self._socket.connect((ip, port))  # Conecta al servidor
```

### Clase Servidor: `Server`
```python
class Server(__Base):
    def __init__(self, ip='localhost', port=27015):
        super().__init__()
        self._socket.bind((ip, port))     # Vincula a dirección
        self._socket.listen(1)            # Escucha conexiones
        self._socket, addr = self._socket.accept()  # Acepta cliente
```

## Módulo de Compresión

### Algoritmo de Compresión

#### Tabla de Caracteres
```python
tabla = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']  # 8 caracteres = 3 bits cada uno
```

#### Proceso de Compresión
1. **Conversión a binario**: Cada carácter → 3 bits
2. **Concatenación**: Unir todos los bits
3. **Padding**: Agregar información de relleno
4. **Empaquetado**: Convertir a bytes

#### Proceso de Descompresión
1. **Lectura de padding**: Primeros 3 bits indican relleno
2. **Extracción de datos**: Quitar bits de relleno
3. **Agrupación**: Dividir en grupos de 3 bits
4. **Conversión**: Cada grupo → carácter de la tabla

## Uso Avanzado

### Cliente Personalizado
```python
from ej_9 import Client

# Conectar a servidor personalizado
cliente = Client(ip='192.168.1.100', port=8080)

# Enviar datos (compresión automática)
cliente.send("ABCDEFGH")

# Recibir respuesta (descompresión automática)
respuesta = cliente.receive()
print(f"Servidor respondió: {respuesta}")

# Cerrar conexión
cliente.close()
```

### Servidor Personalizado
```python
from ej_9 import Server

# Iniciar servidor
servidor = Server(ip='0.0.0.0', port=8080)  # Escucha en todas las interfaces

try:
    # Recibir mensaje del cliente
    mensaje = servidor.receive()
    print(f"Cliente envió: {mensaje}")
    
    # Procesar y responder
    respuesta = f"Recibido: {mensaje}"
    servidor.send(respuesta)
    
finally:
    servidor.close()
```

### Servidor Múltiples Clientes
```python
import threading
from ej_9 import Server

def manejar_cliente():
    servidor = Server()
    try:
        while True:
            mensaje = servidor.receive()
            if not mensaje:
                break
            # Procesar mensaje
            servidor.send(f"Echo: {mensaje}")
    finally:
        servidor.close()

# Crear hilos para múltiples clientes
for i in range(5):
    hilo = threading.Thread(target=manejar_cliente)
    hilo.start()
```

## Análisis de Eficiencia

### Compresión Teórica
- **ASCII estándar**: 8 bits por carácter
- **Compresión personalizada**: 3 bits por carácter
- **Reducción teórica**: (8-3)/8 = 62.5%

### Compresión Real
```python
# Ejemplo con "ABCDEFGH" (8 caracteres)
original_ascii = 8 * 8 = 64 bits
comprimido = 8 * 3 + 3 + padding = 27 + overhead bits
eficiencia_real = variable según padding
```

### Factores que Afectan la Eficiencia
- **Longitud de cadena**: Cadenas más largas son más eficientes
- **Padding**: Overhead fijo por mensaje
- **Overhead de red**: Headers TCP/IP no se comprimen

## Casos de Uso Prácticos

### Transmisión de Códigos
```python
# Códigos de estado usando alfabeto reducido
codigos = {
    "AAAA": "OK",
    "BBBB": "ERROR", 
    "CCCC": "WARNING",
    "DDDD": "INFO"
}

# Transmisión eficiente de códigos predefinidos
cliente.send("AAAA")  # Envía "OK" comprimido
```

### Protocolo de Comandos
```python
# Comandos simples con alfabeto limitado
comandos = {
    "A": "conectar",
    "B": "desconectar",
    "C": "obtener_estado",
    "D": "enviar_datos"
}

# Protocolo minimalista pero funcional
cliente.send("AC")  # Conectar y obtener estado
```

### Sistema de Tokens
```python
# Tokens de autenticación usando alfabeto reducido
def generar_token():
    import random
    alfabeto = "ABCDEFGH"
    return ''.join(random.choice(alfabeto) for _ in range(16))

token = generar_token()  # Ej: "ACBDGHEF..."
cliente.send(token)      # Token comprimido automáticamente
```