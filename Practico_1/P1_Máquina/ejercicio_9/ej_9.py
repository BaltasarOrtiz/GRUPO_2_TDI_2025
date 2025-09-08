"""
9. En la actualidad, muchos de los procesos que se ejecutan en una computadora requiere obtener o enviar
información a otros procesos que se localizan en una computadora diferente, o en la misma. Para lograr esta
comunicación se utilizan los protocolos de comunicación TCP y UDP. Una implementación de comunicación
entre procesos, se puede realizar utilizando sockets.
Los sockets son una forma de comunicación entre procesos que se encuentran en diferentes máquinas de una
red, los sockets proporcionan un punto de comunicación por el cual se puede enviar o recibir información entre
procesos.
Los sockets tienen un ciclo de vida dependiendo si son sockets de servidor, que esperan a un cliente para
establecer una comunicación, o socket cliente que busca a un socket de servidor para establecer la
comunicación.
Haciendo uso de sockets, implemente un servidor y un cliente (a modo de ejemplo, se proveen un servidor y un
cliente en lenguaje Python), que permita desde el cliente, enviar un archivo comprimido utilizando el alfabeto
ABCDEFGH, y en el servidor, descomprimir el archivo.
"""
import Compresor
import socket

class __Base:
	"""Clase base que proporciona funcionalidad común para cliente y servidor."""
	_socket = None
	
	def __init__(self):
		"""Inicializa un socket TCP."""
		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def send(self, string):
		"""
		Comprime y envía una cadena a través del socket.
		
		Args:
			string (str): Cadena a comprimir y enviar
		"""
		self._socket.send(Compresor.compress(string))

	def receive(self):
		"""
		Recibe datos del socket y los descomprime.
		
		Returns:
			str: Cadena descomprimida recibida
		"""
		return Compresor.decompress(self._socket.recv(1024))

	def close(self):
		"""Cierra la conexión del socket."""
		self._socket.close()

class Client(__Base):
	"""Cliente que se conecta a un servidor para enviar/recibir datos comprimidos."""
	
	def __init__(self, ip = 'localhost', port = 27015):
		"""
		Inicializa el cliente y se conecta al servidor.
		
		Args:
			ip (str): Dirección IP del servidor (por defecto 'localhost')
			port (int): Puerto del servidor (por defecto 27015)
		"""
		super().__init__()
		self._socket.connect((ip, port))
		
class Server(__Base):
	"""Servidor que acepta conexiones de clientes para recibir/enviar datos comprimidos."""
	
	def __init__(self, ip = 'localhost', port = 27015):
		"""
		Inicializa el servidor, lo vincula a una dirección y acepta una conexión.
		
		Args:
			ip (str): Dirección IP para vincular el servidor (por defecto 'localhost')
			port (int): Puerto para vincular el servidor (por defecto 27015)
		"""
		super().__init__()
		self._socket.bind((ip, port))  # Vincula el socket a la dirección
		self._socket.listen(1)         # Escucha hasta 1 conexión pendiente
		self._socket, addr = self._socket.accept()  # Acepta la primera conexión

if __name__ == "__main__":
	import threading
	
	def make_server():
		"""
		Función que ejecuta el servidor en un hilo separado.
		Recibe un mensaje del cliente y envía dos respuestas.
		"""
		server = Server()
		recibido = server.receive()  # Recibe mensaje comprimido del cliente
		server.send("ABCDE")         # Envía primera respuesta comprimida
		server.send("AAAA" + recibido)  # Envía segunda respuesta (concatena con lo recibido)
		server.close()
		
	# Crear y ejecutar el servidor en un hilo separado para evitar bloqueo
	thread = threading.Thread(target=make_server)
	thread.start()
	
	# Crear el cliente y enviar datos comprimidos al servidor
	client = Client()
	client.send("BDAEB")  # Envía mensaje comprimido usando alfabeto ABCDEFGH
	
	# Recibir y mostrar las dos respuestas del servidor (ya descomprimidas)
	print(client.receive())  # Recibe "ABCDE"
	print(client.receive())  # Recibe "AAAA" + mensaje original
	
	# Cerrar la conexión del cliente y esperar a que termine el hilo del servidor
	client.close()
	thread.join()
    