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


pwds = ["123456", "SEEDsa!23_", "_ClaUdeIA!2", "AswE2a", "abc123"]

for pwd in pwds:
    print(verificar_pwd(pwd))

    
    sugerencias = []
    if not tiene_numero:
        sugerencias.append("agregá al menos un número")
    if not tiene_mayuscula:
        sugerencias.append("agregá al menos una mayúscula")
    if not tiene_especial:
        sugerencias.append("agregá un carácter especial")
    if len(pwd) < 8:
        sugerencias.append("usá al menos 8 caracteres")
    
    return resultado, sugerencias


