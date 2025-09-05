"""
5. Desarrollar una aplicación de software que almacene en un archivo los siguientes datos de personas: Apellido y nombre, dirección, dni y 8 campos bivaluados, del tipo S/N o True/False, por ejemplo: estudios primarios (S/N), estudios secundarios (S/N), estudios universitarios (S/N), tiene vivienda propia (S/N), obra social (S/N), trabaja (S/N), etc. El programa desarrollado deberá permitir: 
	a) almacenar y recuperar los datos en un archivo con campos de longitud fija (archivo "fijos dat").
	b) almacenar y recuperar los datos en un archivo de longitud variable (archivo "variable dat"). Ingresar los mismos datos en ambos archivos para unas 20 (veinte) personas, comparar el tamaño de ambos archivos.
"""
import os
import struct

# Definimos la estructura para los datos de una persona
class Persona:
	def __init__(self, nombre, direccion, dni, estudios, vivienda, etc):
		self.nombre = nombre
		self.direccion = direccion
		self.dni = dni
		# Almacenamos los 8 campos S/N como una lista de booleanos
		self.campos_sn = estudios + vivienda + etc

def guardar_longitud_fija(personas, nombre_archivo="fijos.dat"):
	"""
	Guarda una lista de personas en un archivo con campos de longitud fija.
	"""
	# Obtenemos el directorio del script actual
	directorio_script = os.path.dirname(os.path.abspath(__file__))
	ruta_completa = os.path.join(directorio_script, nombre_archivo)
	
	# Definimos la estructura fija:
	# - 50s: string de 50 bytes para el nombre
	# - 60s: string de 60 bytes para la dirección
	# - 10s: string de 10 bytes para el DNI
	# - B: 1 byte (entero sin signo) para empaquetar los 8 booleanos
	# El tamaño total del registro será 50 + 60 + 10 + 1 = 121 bytes
	formato = '50s 60s 10s B'
	
	with open(ruta_completa, 'wb') as f:
		for p in personas:
			# Empaquetamos los 8 booleanos en un solo byte usando operaciones de bits
			campos_empaquetados = 0
			for i, valor in enumerate(p.campos_sn):
				if valor:
					campos_empaquetados |= (1 << i)

			# Escribimos el registro empaquetado en el archivo
			registro = struct.pack(formato, 
								   p.nombre.encode('utf-8'), 
								   p.direccion.encode('utf-8'), 
								   p.dni.encode('utf-8'),
								   campos_empaquetados)
			f.write(registro)

def guardar_longitud_variable(personas, nombre_archivo="variable.dat"):
	"""
	Guarda una lista de personas en un archivo con campos de longitud variable,
	usando un delimitador (estilo CSV).
	"""
	# Obtenemos el directorio del script actual
	directorio_script = os.path.dirname(os.path.abspath(__file__))
	ruta_completa = os.path.join(directorio_script, nombre_archivo)
	
	with open(ruta_completa, 'w', encoding='utf-8') as f:
		for p in personas:
			# Convertimos la lista de booleanos a una cadena de S/N
			campos_str = ['S' if valor else 'N' for valor in p.campos_sn]
			# Unimos todos los campos con una coma y escribimos una línea por persona
			linea = ";".join([p.nombre, p.direccion, p.dni] + campos_str)
			f.write(linea + '\n')

# --- Inicio del programa ---
if __name__ == "__main__":
	# Obtenemos el directorio del script actual para las comparaciones
	directorio_script = os.path.dirname(os.path.abspath(__file__))
	
	# 1. Generar 20 registros de ejemplo
	personas_ejemplo = []
	for i in range(1, 21):
		# Datos de ejemplo que varían en longitud
		nombre = f"Apellido{i} Nombre{i}"
		direccion = f"Calle Falsa {i*10}, Ciudad"
		dni = f"30{i:06d}" # DNI de 8 dígitos
		# Campos booleanos de ejemplo
		estudios = [True, i % 2 == 0, i % 5 == 0]
		vivienda = [i % 3 == 0]
		etc = [True, False, True, i > 10]
		
		personas_ejemplo.append(Persona(nombre, direccion, dni, estudios, vivienda, etc))

	# 2. Guardar los datos usando ambos métodos
	guardar_longitud_fija(personas_ejemplo)
	guardar_longitud_variable(personas_ejemplo)

	# 3. Comparar los tamaños de los archivos generados
	archivo_fijo = os.path.join(directorio_script, "fijos.dat")
	archivo_variable = os.path.join(directorio_script, "variable.dat")
	
	tamano_fijo = os.path.getsize(archivo_fijo)
	tamano_variable = os.path.getsize(archivo_variable)

	print("--- Comparación de Tamaños de Archivo ---")
	print(f"Archivo de longitud fija ('fijos.dat'):    {tamano_fijo} bytes")
	print(f"Archivo de longitud variable ('variable.dat'): {tamano_variable} bytes")
	print("-" * 40)
	
	if tamano_variable < tamano_fijo:
		diferencia = tamano_fijo - tamano_variable
		print(f"El archivo de longitud variable es {diferencia} bytes más pequeño.")
		print("Esto demuestra la eficiencia en espacio de los registros variables.")
	else:
		print("Ambos archivos tienen un tamaño similar.")