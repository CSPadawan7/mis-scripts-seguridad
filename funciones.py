def verificar_pwd(pwd):

    especiales = "_-!@#$%&*"

    tiene_numero = False
    tiene_mayuscula = False
    tiene_especial = False

    puntos = 0

    for caracter in pwd:

        if caracter.isdigit():
            tiene_numero = True

        if caracter.isupper():
            tiene_mayuscula = True

        if caracter in especiales:
            tiene_especial = True

    if len(pwd) >= 9:
        puntos += 1

    if tiene_numero:
        puntos += 1

    if tiene_mayuscula:
        puntos += 1

    if tiene_especial:
        puntos += 1

    if puntos <= 2:
        return "Débil"

    elif puntos == 3:
        return "Media"

    else:
        return "Fuerte"

pwd = input("Escribe tu contraseña: ")

resultado = verificar_pwd(pwd)

print(f"Seguridad de la contraseña: {resultado}")
    
    

