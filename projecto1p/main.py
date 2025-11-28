import math

# VARIABLES PRINCIPALES
cadenas_originales = []
cadenas_codificadas = []
datos_metadata = []

# FUNCION DE CARGA
def cargar_datos():
    global cadenas_originales

    print("1.Manual \n2.Archivo")
    opcion = int(input("Ingresa una opcion: "))

    if opcion == 1:
        linea = "linea :)"
        while linea != "FIN":
            linea = input("Ingrese cadena (FIN para terminar):")
            if es_numerico(linea.strip()):
                cadenas_originales.append(linea)
    else:
        nombre_archivo = input("Archivo: ")
        ruta = "archivos/" + nombre_archivo
        with open(ruta, "r", encoding="utf-8") as archivo:
            for linea in archivo:
                if es_numerico(linea.strip()):
                    cadenas_originales.append(linea.rstrip() + "\n")
        archivo.close()

    print("Cargadas: ", len(cadenas_originales))
    if len(cadenas_originales) <= 10:
        mostrar_lista(cadenas_originales)

# FUNCIONES DE CODIFICACION
def codificar_cadena(cadena: str):
    ancho = calcular_ancho(len(cadena))
    simbolos = dividir_bloques(cadena, ancho)

    resultado = []
    vistos = set()
    usados = set()
    metadata = []

    for pos in range(len(simbolos)):
        simbolo = simbolos[pos]

        if simbolo not in vistos:
            resultado.append(simbolo)
            vistos.add(simbolo)
            usados.add(simbolo)
        else:
            reemplazo = buscar_vecino(simbolo, usados, ancho)
            resultado.append(reemplazo)
            usados.add(reemplazo)
            metadata.append((pos, simbolo, reemplazo))
    return {
        "codificada": "".join(resultado),
        "metadata": metadata,
        "ancho": ancho
    }

def procesar_codificacion():
    global cadenas_originales
    global cadenas_codificadas
    global datos_metadata

    if len(cadenas_originales) == 0:
        print("\nSin datos\n")
        return

    for cadena in cadenas_originales:
        resultado = codificar_cadena(cadena)
        cadenas_codificadas.append(resultado["codificada"])
        datos_metadata.append(resultado)

    if len(cadenas_originales) <= 10:
        mostrar_resultados_codificacion()
    else:
        guardar_archivo("codificadas.txt", cadenas_codificadas, cadenas_originales)



# FUNCIONES DE DECODIFICACION
def procesar_decodificacion():
    global cadenas_codificadas
    global datos_metadata

    if len(cadenas_codificadas) == 0:
        print("\nSin datos codificados\n")
        return

    decodificadas = []

    for dato in datos_metadata:
        simbolos = dividir_bloques(dato["codificada"], dato["ancho"])

        for (pos, original, reemplazo) in dato["metadata"]:
            simbolos[pos] = original

        decodificadas.append("".join(simbolos))

    if len(cadenas_codificadas) <= 10:
        mostrar_resultados_decodificacion(decodificadas)
    else:
        guardar_archivo("decodificadas.txt", decodificadas, cadenas_codificadas)

# FUNCIONES AUXILIARES PRINCIPALES
def calcular_ancho(n: int) -> int:
    if (n <= 10):
        return 1
    elif (n <= 66):
        return 2
    elif (n <= 666):
        return 3
    else:
        return math.ceil(math.log10(n * 1.5))

def dividir_bloques(cadena: str, ancho: int) -> list[str]:
    bloques = []

    for i in range(0, len(cadena), ancho):
        bloque = cadena[i:i + ancho]
        while len(bloque) < ancho:
            bloque = bloque + "0"
        bloques.append(bloque)

    return bloques

def buscar_vecino(simbolo: str, usados: set, ancho: int) -> str:
    valor = int(simbolo)
    max_val = (10 ** ancho) - 1

    for dist in range(1, max_val + 1):
        izq = valor - dist
        if izq >= 0:
            candidato = formatear(izq, ancho)
            if candidato not in usados:
                return candidato

        der = valor + dist
        if der <= max_val:
            candidato = formatear(der, ancho)
            if candidato not in usados:
                return candidato

    return formatear(0, ancho)

def formatear(valor: int, ancho: int) -> str:
    s = str(valor)
    while len(s) < ancho:
        s = "0" + s

    return s

# FUNCIONES DE VISUALIZACION
def mostrar_lista(lista: list[str]):
    limite = min(len(lista), 10)

    for i in range(limite):
        print(f"{i + 1}. {lista[i]}")

def mostrar_resultados_codificacion():
    print("=== CODIFICACIÓN ===")

    for i in range(len(cadenas_originales)):
        print("Original:   ", cadenas_originales[i])
        print("Codificada: ", cadenas_codificadas[i])
        print("")

def mostrar_resultados_decodificacion(decodificadas: list[str]):
    print("=== DECODIFICACIÓN ===")

    for i in range(len(decodificadas)):
        print("Codificada:   ", cadenas_codificadas[i])
        print("Decodificada: ", decodificadas[i])

        if decodificadas[i] == cadenas_originales[i]:
            print("Estado: OK")

        print("")

def guardar_archivo(nombre: str, datos1: list, datos2: list):
    ruta = "archivos/" + nombre
    archivo = open(ruta, "w", encoding="utf-8")
    i = 0
    for i in range(len(datos1)):
        archivo.write(f"Cadena {i + 1}\n")
        archivo.write(datos2[i])
        archivo.write(datos1[i])
        archivo.write("\n")

    archivo.close()
    print("Guardado en:", nombre)

def es_numerico(s: str) -> bool:
    for c in s:
        if c < '0' or c > '9':
            return False
    return True


# PROGRAMA PRINCIPAL
def main():
    salir = 0
    while (salir != 1):
        print("MENÚ: \n1.Cargar \n2.Codificar \n3.Decodificar \n4.Salir")
        opcion = int(input("Ingresa una opcion: "))

        match opcion:
            case 1:
                cargar_datos()
            case 2:
                procesar_codificacion()
            case 3:
                procesar_decodificacion()
            case 4:
                salir = 1

if __name__ == "__main__":
    main()
