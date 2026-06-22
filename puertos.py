#Ejercicio de lista de puertos con blucles for

continuar = "si"

while continuar == "si":

    puertos = [644,750, 641, 332, 21, 22, 23, 80, 443, 445, 3389]

    for puerto in puertos:

        if puerto in [23, 445, 3389]:
            print(f"Puerto {puerto}: Alto riesgo, conexión denegada")

        elif puerto in [21, 80]:
            print(f"Puerto {puerto}: Precacución, proceda con cuidado")

        else:
            print(f"Puerto {puerto}: Seguro, conexión permitida")

    continuar = input("¿Deseas volver a analizar? (si/no): ")
