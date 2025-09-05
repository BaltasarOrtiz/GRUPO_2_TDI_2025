"""
9. En la actualidad, muchos de los procesos que se ejecutan en una computadora requiere obtener o enviar información a otros procesos que se localizan en una computadora diferente, o en la misma. Para lograr esta comunicación se utilizan los protocolos de comunicación TCP y UDP. Una implementación de comunicación entre procesos, se puede realizar utilizando sockets.
Los sockets son una forma de comunicación entre procesos que se encuentran en diferentes máquinas de una red, los sockets proporcionan un punto de comunicación por el cual se puede enviar o recibir información entre procesos.
Los sockets tienen un ciclo de vida dependiendo si son sockets de servidor, que esperan a un cliente para establecer una comunicación, o socket cliente que busca a un socket de servidor para establecer la comunicación.
Haciendo uso de sockets, implemente un servidor y un cliente (a modo de ejemplo, se proveen un servidor y un cliente en lenguaje Python), que permita desde el cliente, enviar un archivo comprimido utilizando el alfabeto ABCDEFGH, y en el servidor, descomprimir el archivo.
"""
import socket

# Diccionario para la descompresión: convierte un código de 3 bits a un caracter
CODIGOS_DECOMP = {
    '000': 'A', '001': 'B', '010': 'C', '011': 'D',
    '100': 'E', '101': 'F', '110': 'G', '111': 'H'
}

def descomprimir(datos_bytes):
    """
    Descomprime los datos recibidos (bytes) a texto usando códigos de 3 bits.
    """
    # 1. Convertir todos los bytes recibidos a una sola cadena de bits
    cadena_bits = "".join(f"{byte:08b}" for byte in datos_bytes)
    
    # 2. Leer la longitud del padding del primer byte
    num_padding_bits = int(cadena_bits[:8], 2)
    cadena_bits_utiles = cadena_bits[8:]
    
    # 3. Eliminar los bits de padding del final
    if num_padding_bits > 0:
        cadena_bits_utiles = cadena_bits_utiles[:-num_padding_bits]
        
    # 4. Decodificar la cadena de bits en grupos de 3
    texto_descomprimido = ""
    for i in range(0, len(cadena_bits_utiles), 3):
        chunk = cadena_bits_utiles[i:i+3]
        if chunk in CODIGOS_DECOMP:
            texto_descomprimido += CODIGOS_DECOMP[chunk]
            
    return texto_descomprimido

def iniciar_servidor(ip="0.0.0.0", puerto=5555):
    """
    Inicia el servidor para recibir un archivo comprimido.
    """
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((ip, puerto))
    servidor.listen(1) # Escuchar solo 1 conexión a la vez
    print(f"[*] Esperando conexiones en {ip}:{puerto}")

    cliente_socket, direccion = servidor.accept()
    print(f"[*] Conexión establecida con {direccion[0]}:{direccion[1]}")

    # Recibir los datos del cliente
    datos_recibidos = b""
    while True:
        parte = cliente_socket.recv(1024)
        if not parte:
            break
        datos_recibidos += parte
    
    print(f"[*] Se recibieron {len(datos_recibidos)} bytes de datos comprimidos.")

    # Descomprimir los datos y guardarlos en un archivo
    texto_final = descomprimir(datos_recibidos)
    with open("archivo_recibido.txt", "w") as f:
        f.write(texto_final)
    
    print("[*] Archivo descomprimido y guardado como 'archivo_recibido.txt'.")
    
    # Cerrar conexiones
    cliente_socket.close()
    servidor.close()
    print("[*] Conexiones cerradas. Servidor apagado.")

if __name__ == "__main__":
    iniciar_servidor()