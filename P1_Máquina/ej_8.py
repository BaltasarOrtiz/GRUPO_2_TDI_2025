"""
8. Implementar un programa que valide un CUIT/CUIL ingresado por teclado.
"""
def validar_cuit_cuil(cuit):
    """
    Valida un número de CUIT/CUIL argentino.

    Args:
        cuit (str): El CUIT/CUIL a validar, puede tener guiones.

    Returns:
        bool: True si es válido, False en caso contrario.
    """
    # 1. Limpiar el CUIT de guiones y espacios
    cuit_limpio = cuit.replace('-', '').replace(' ', '')

    # 2. Verificar que tenga 11 dígitos y que sean todos numéricos
    if len(cuit_limpio) != 11 or not cuit_limpio.isdigit():
        return False

    # 3. El algoritmo de validación
    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
    acumulado = 0

    # Calculamos la suma ponderada de los primeros 10 dígitos
    for i in range(10):
        acumulado += int(cuit_limpio[i]) * base[i]

    # Calculamos el resto de la división por 11
    resto = acumulado % 11
    
    # Calculamos el dígito verificador esperado
    digito_esperado = 11 - resto
    if digito_esperado == 11:
        digito_esperado = 0
    elif digito_esperado == 10:
        # Un resultado de 10 es inválido. A veces se recalcula con otra base
        # o se asigna un CUIT diferente, pero para la validación estándar, falla.
        return False

    # 4. Comparamos el dígito calculado con el último dígito del CUIT
    digito_verificador = int(cuit_limpio[10])
    
    return digito_esperado == digito_verificador

# --- Inicio del programa ---
if __name__ == "__main__":
    print("--- Validador de CUIT/CUIL de Argentina ---")
    numero_cuit = input("Ingresa el CUIT/CUIL a validar (con o sin guiones): ")

    if validar_cuit_cuil(numero_cuit):
        print(f"✅ El CUIT/CUIL '{numero_cuit}' es VÁLIDO.")
    else:
        print(f"❌ El CUIT/CUIL '{numero_cuit}' es INVÁLIDO.")