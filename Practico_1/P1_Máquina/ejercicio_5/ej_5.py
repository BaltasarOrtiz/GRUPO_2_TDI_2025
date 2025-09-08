"""
5. Desarrollar una aplicación de software que almacene en un archivo los siguientes datos de personas: Apellido y nombre, dirección, dni y 8 campos bivaluados, del tipo S/N o True/False, por ejemplo: estudios primarios (S/N), estudios secundarios (S/N), estudios universitarios (S/N), tiene vivienda propia (S/N), obra social (S/N), trabaja (S/N), etc. El programa desarrollado deberá permitir: 
	a) almacenar y recuperar los datos en un archivo con campos de longitud fija (archivo "fijos dat").
	b) almacenar y recuperar los datos en un archivo de longitud variable (archivo "variable dat"). Ingresar los mismos datos en ambos archivos para unas 20 (veinte) personas, comparar el tamaño de ambos archivos.
"""
import os
import struct

# Definimos la estructura para los datos de una persona
class Persona:
	"""
	Clase que representa los datos de una persona con campos fijos y variables.
	
	Attributes:
		nombre (str): Apellido y nombre de la persona
		direccion (str): Dirección de residencia
		dni (str): Documento Nacional de Identidad
		campos_sn (list): Lista de 8 valores booleanos para campos S/N
	"""
	def __init__(self, nombre, direccion, dni, estudios, vivienda, etc):
		"""
		Inicializa una nueva instancia de Persona.
		
		Args:
			nombre (str): Apellido y nombre completo
			direccion (str): Dirección de la persona
			dni (str): DNI como string
			estudios (list): Lista de booleanos para estudios (primarios, secundarios, universitarios)
			vivienda (list): Lista de booleanos para vivienda propia
			etc (list): Lista de booleanos para otros campos (obra social, trabajo, etc.)
		"""
		self.nombre = nombre
		self.direccion = direccion
		self.dni = dni
		# Concatenamos las listas para formar los 8 campos S/N como booleanos
		self.campos_sn = estudios + vivienda + etc

def guardar_longitud_fija(personas, nombre_archivo="fijos.dat"):
	"""
	Guarda una lista de personas en un archivo con campos de longitud fija.
	Cada registro ocupa exactamente el mismo espacio en disco.
	
	Args:
		personas (list): Lista de objetos Persona a guardar
		nombre_archivo (str): Nombre del archivo donde guardar los datos
	
	Estructura del archivo:
		- Cada registro: 121 bytes fijos
		- Nombre: 50 bytes (padded con nulls si es menor)
		- Dirección: 60 bytes (padded con nulls si es menor)
		- DNI: 10 bytes (padded con nulls si es menor)
		- Campos S/N: 1 byte (8 bits para 8 campos booleanos)
	"""
	# Obtenemos el directorio del script actual para crear archivos relativos
	directorio_script = os.path.dirname(os.path.abspath(__file__))
	ruta_completa = os.path.join(directorio_script, nombre_archivo)
	
	# Definimos la estructura fija usando el formato de struct:
	# - 50s: string de 50 bytes para el nombre (apellido y nombre)
	# - 60s: string de 60 bytes para la dirección
	# - 10s: string de 10 bytes para el DNI
	# - B: 1 byte (unsigned char) para empaquetar los 8 booleanos
	# Tamaño total del registro: 50 + 60 + 10 + 1 = 121 bytes por persona
	formato = '50s 60s 10s B'
	
	with open(ruta_completa, 'wb') as f:
		for p in personas:
			# Empaquetamos los 8 campos booleanos en un solo byte usando operaciones de bits
			# Cada bit representa un campo S/N (True=1, False=0)
			campos_empaquetados = 0
			for i, valor in enumerate(p.campos_sn):
				if valor:
					# Establecemos el bit en la posición i si el valor es True
					campos_empaquetados |= (1 << i)

			# Empaquetamos y escribimos el registro completo en formato binario
			# struct.pack convierte los datos a bytes según el formato especificado
			registro = struct.pack(formato, 
								   p.nombre.encode('utf-8'),     # Convertimos string a bytes
								   p.direccion.encode('utf-8'),  # Convertimos string a bytes
								   p.dni.encode('utf-8'),        # Convertimos string a bytes
								   campos_empaquetados)          # Ya es un entero (0-255)
			f.write(registro)

def guardar_longitud_variable(personas, nombre_archivo="variable.dat"):
	"""
	Guarda una lista de personas en un archivo con campos de longitud variable.
	Utiliza formato tipo CSV con delimitadores, ocupando solo el espacio necesario.
	
	Args:
		personas (list): Lista de objetos Persona a guardar
		nombre_archivo (str): Nombre del archivo donde guardar los datos
	
	Formato del archivo:
		- Una línea por persona
		- Campos separados por punto y coma (;)
		- Campos S/N representados como 'S' o 'N'
		- Codificación UTF-8 para soportar caracteres especiales
	"""
	# Obtenemos el directorio del script actual para crear archivos relativos
	directorio_script = os.path.dirname(os.path.abspath(__file__))
	ruta_completa = os.path.join(directorio_script, nombre_archivo)
	
	with open(ruta_completa, 'w', encoding='utf-8') as f:
		for p in personas:
			# Convertimos la lista de booleanos a una lista de strings 'S'/'N'
			campos_str = ['S' if valor else 'N' for valor in p.campos_sn]
			
			# Unimos todos los campos con punto y coma como delimitador
			# Formato: "Nombre;Dirección;DNI;Campo1;Campo2;...;Campo8"
			linea = ";".join([p.nombre, p.direccion, p.dni] + campos_str)
			
			# Escribimos la línea completa seguida de un salto de línea
			f.write(linea + '\n')

# --- Programa principal ---
if __name__ == "__main__":
	# Obtenemos el directorio del script actual para las operaciones de archivo
	directorio_script = os.path.dirname(os.path.abspath(__file__))
	
	# 1. Generamos 20 registros de ejemplo con datos variados
	print("Generando 20 registros de ejemplo...")
	personas_ejemplo = []
	
	for i in range(1, 21):
		# Creamos datos de ejemplo que varían en longitud para probar eficiencia
		nombre = f"Apellido{i} Nombre{i}"
		direccion = f"Calle Falsa {i*10}, Ciudad"
		dni = f"30{i:06d}"  # DNI de 8 dígitos: 30000001, 30000002, etc.
		
		# Generamos campos booleanos de ejemplo con patrones variados:
		estudios = [
			True,           # Estudios primarios (siempre True)
			i % 2 == 0,     # Estudios secundarios (números pares)
			i % 5 == 0      # Estudios universitarios (múltiplos de 5)
		]
		vivienda = [
			i % 3 == 0      # Vivienda propia (múltiplos de 3)
		]
		etc = [
			True,           # Obra social (siempre True)
			False,          # Campo adicional 1 (siempre False)
			True,           # Campo adicional 2 (siempre True)
			i > 10          # Campo adicional 3 (personas 11-20)
		]
		
		# Verificamos que tenemos exactamente 8 campos booleanos
		total_campos = len(estudios) + len(vivienda) + len(etc)
		assert total_campos == 8, f"Se requieren exactamente 8 campos, se encontraron {total_campos}"
		
		personas_ejemplo.append(Persona(nombre, direccion, dni, estudios, vivienda, etc))

	# 2. Guardamos los datos usando ambos métodos de almacenamiento
	print("Guardando datos en archivo de longitud fija...")
	guardar_longitud_fija(personas_ejemplo)
	
	print("Guardando datos en archivo de longitud variable...")
	guardar_longitud_variable(personas_ejemplo)

	# 3. Comparamos los tamaños de los archivos generados
	archivo_fijo = os.path.join(directorio_script, "fijos.dat")
	archivo_variable = os.path.join(directorio_script, "variable.dat")
	
	# Obtenemos el tamaño en bytes de cada archivo
	tamano_fijo = os.path.getsize(archivo_fijo)
	tamano_variable = os.path.getsize(archivo_variable)

	# Mostramos los resultados de la comparación
	print("\n" + "="*50)
	print("     COMPARACIÓN DE TAMAÑOS DE ARCHIVO")
	print("="*50)
	print(f"Archivo de longitud fija ('fijos.dat'):      {tamano_fijo:,} bytes")
	print(f"Archivo de longitud variable ('variable.dat'): {tamano_variable:,} bytes")
	print("-" * 50)
	
	# Calculamos y mostramos la diferencia
	if tamano_variable < tamano_fijo:
		diferencia = tamano_fijo - tamano_variable
		porcentaje_ahorro = (diferencia / tamano_fijo) * 100
		print(f"✓ El archivo de longitud variable es {diferencia:,} bytes más pequeño.")
		print(f"✓ Esto representa un ahorro del {porcentaje_ahorro:.1f}% en espacio de almacenamiento.")
		print("✓ Demuestra la eficiencia en espacio de los registros de longitud variable.")
	elif tamano_fijo < tamano_variable:
		diferencia = tamano_variable - tamano_fijo
		porcentaje_extra = (diferencia / tamano_fijo) * 100
		print(f"⚠ El archivo de longitud fija es {diferencia:,} bytes más pequeño.")
		print(f"⚠ El archivo variable ocupa {porcentaje_extra:.1f}% más espacio.")
		print("⚠ Esto puede ocurrir con pocos registros debido al overhead de delimitadores.")
	else:
		print("➤ Ambos archivos tienen exactamente el mismo tamaño.")
	
	print("="*50)
	print(f"Registros procesados: {len(personas_ejemplo)}")
	print(f"Bytes por registro (fijo): {tamano_fijo // len(personas_ejemplo)}")
	print(f"Bytes promedio por registro (variable): {tamano_variable // len(personas_ejemplo)}")