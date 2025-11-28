#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Codificador/Decodificador de Cadenas Numéricas
Proyecto de Análisis de Algoritmos
"""

import math
import os

# ============================================================================
# VARIABLES GLOBALES (Capa de Datos)
# ============================================================================
cadenas_originales = []
cadenas_codificadas = []
datos_metadata = []


# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def es_numerico(s):
    """
    Verifica si una cadena contiene únicamente dígitos.
    
    Args:
        s (str): Cadena a verificar
        
    Returns:
        bool: True si todos los caracteres son dígitos, False en caso contrario
    """
    if not s:  # Cadena vacía
        return False
    return all(c.isdigit() for c in s)


def calcular_ancho(n):
    """
    Calcula el ancho óptimo para dividir una cadena en símbolos.
    
    Args:
        n (int): Longitud de la cadena
        
    Returns:
        int: Ancho del símbolo
    """
    if n <= 10:
        return 1
    elif n <= 66:
        return 2
    elif n <= 666:
        return 3
    else:
        return math.ceil(math.log10(n * 1.5))


def formatear(valor, ancho):
    """
    Formatea un número entero como string con ceros a la izquierda.
    
    Args:
        valor (int): Número a formatear
        ancho (int): Ancho total del string resultante
        
    Returns:
        str: Número formateado con ceros a la izquierda
    """
    return str(valor).zfill(ancho)


def dividir_bloques(cadena, ancho):
    """
    Divide una cadena en bloques de tamaño fijo, rellenando con ceros si es necesario.
    
    Args:
        cadena (str): Cadena a dividir
        ancho (int): Tamaño de cada bloque
        
    Returns:
        list: Lista de strings con los bloques
    """
    bloques = []
    for i in range(0, len(cadena), ancho):
        bloque = cadena[i:i+ancho]
        # Rellenar con ceros si el último bloque es más corto
        bloque = bloque.ljust(ancho, '0')
        bloques.append(bloque)
    return bloques


def buscar_vecino(simbolo, usados, ancho):
    """
    Busca el símbolo más cercano no usado, alternando entre izquierda y derecha.
    
    Args:
        simbolo (str): Símbolo repetido que necesita reemplazo
        usados (set): Conjunto de símbolos ya utilizados
        ancho (int): Ancho del símbolo
        
    Returns:
        str: Símbolo sustituto más cercano no usado
    """
    valor = int(simbolo)
    max_val = (10 ** ancho) - 1
    
    for dist in range(1, max_val + 1):
        # Intentar a la izquierda
        izq = valor - dist
        if izq >= 0:
            candidato_izq = formatear(izq, ancho)
            if candidato_izq not in usados:
                return candidato_izq
        
        # Intentar a la derecha
        der = valor + dist
        if der <= max_val:
            candidato_der = formatear(der, ancho)
            if candidato_der not in usados:
                return candidato_der
    
    # Si no encuentra ninguno (caso extremo), retornar "0...0"
    return formatear(0, ancho)


# ============================================================================
# FUNCIONES DE CODIFICACIÓN
# ============================================================================

def codificar_cadena(cadena):
    """
    Codifica una cadena reemplazando símbolos repetidos por vecinos no usados.
    
    Args:
        cadena (str): Cadena numérica a codificar
        
    Returns:
        dict: Diccionario con 'codificada', 'metadata' y 'ancho'
    """
    ancho = calcular_ancho(len(cadena))
    simbolos = dividir_bloques(cadena, ancho)
    
    resultado = []
    vistos = set()
    usados = set()
    metadata = []
    
    for pos, simbolo in enumerate(simbolos):
        if simbolo not in vistos:
            # Primera aparición del símbolo
            resultado.append(simbolo)
            vistos.add(simbolo)
            usados.add(simbolo)
        else:
            # Símbolo repetido: buscar reemplazo
            reemplazo = buscar_vecino(simbolo, usados, ancho)
            resultado.append(reemplazo)
            usados.add(reemplazo)
            # Guardar información para decodificar
            metadata.append((pos, simbolo, reemplazo))
    
    return {
        'codificada': ''.join(resultado),
        'metadata': metadata,
        'ancho': ancho
    }


def procesar_codificacion():
    """
    Procesa la codificación de todas las cadenas originales cargadas.
    """
    global cadenas_codificadas, datos_metadata
    
    if not cadenas_originales:
        print("\n❌ Error: No hay datos cargados. Use la opción 1 primero.")
        return
    
    print("\n🔄 Procesando codificación...")
    cadenas_codificadas = []
    datos_metadata = []
    
    for cadena in cadenas_originales:
        resultado = codificar_cadena(cadena)
        cadenas_codificadas.append(resultado['codificada'])
        datos_metadata.append(resultado)
    
    print(f"✅ Codificación completada: {len(cadenas_codificadas)} cadenas procesadas.\n")
    
    # Mostrar resultados según el tamaño
    if len(cadenas_originales) <= 10:
        mostrar_resultados_codificacion()
    else:
        guardar_archivo("codificadas.txt", cadenas_codificadas, cadenas_originales, "codificación")


# ============================================================================
# FUNCIONES DE DECODIFICACIÓN
# ============================================================================

def procesar_decodificacion():
    """
    Procesa la decodificación de todas las cadenas codificadas.
    """
    if not cadenas_codificadas:
        print("\n❌ Error: No hay datos codificados. Use la opción 2 primero.")
        return
    
    print("\n🔄 Procesando decodificación...")
    decodificadas = []
    
    for dato in datos_metadata:
        simbolos = dividir_bloques(dato['codificada'], dato['ancho'])
        
        # Aplicar metadata para restaurar símbolos originales
        for pos, original, reemplazo in dato['metadata']:
            simbolos[pos] = original
        
        decodificadas.append(''.join(simbolos))
    
    print(f"✅ Decodificación completada: {len(decodificadas)} cadenas procesadas.\n")
    
    # Mostrar resultados según el tamaño
    if len(cadenas_codificadas) <= 10:
        mostrar_resultados_decodificacion(decodificadas)
    else:
        guardar_archivo("decodificadas.txt", decodificadas, cadenas_codificadas, "decodificación")


# ============================================================================
# FUNCIONES DE CARGA DE DATOS
# ============================================================================

def cargar_datos():
    """
    Gestiona la carga de datos desde entrada manual o archivo.
    """
    global cadenas_originales
    
    print("\n" + "="*50)
    print("CARGA DE DATOS")
    print("="*50)
    print("1. Entrada manual")
    print("2. Cargar desde archivo")
    print("-"*50)
    
    try:
        opcion = int(input("Seleccione una opción: "))
    except ValueError:
        print("❌ Opción inválida.")
        return
    
    cadenas_originales = []
    
    if opcion == 1:
        print("\n📝 Ingrese cadenas numéricas (escriba 'FIN' para terminar):")
        while True:
            linea = input("► ").strip()
            if linea.upper() == "FIN":
                break
            if es_numerico(linea):
                cadenas_originales.append(linea)
            else:
                print("  ⚠️  Cadena inválida (solo se permiten dígitos). Ignorada.")
    
    elif opcion == 2:
        nombre_archivo = input("\n📁 Ingrese el nombre del archivo: ").strip()
        try:
            with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if es_numerico(linea):
                        cadenas_originales.append(linea)
            print(f"✅ Archivo '{nombre_archivo}' leído correctamente.")
        except FileNotFoundError:
            print(f"❌ Error: El archivo '{nombre_archivo}' no existe.")
            return
        except Exception as e:
            print(f"❌ Error al leer el archivo: {e}")
            return
    else:
        print("❌ Opción inválida.")
        return
    
    # Confirmar carga
    print(f"\n✅ Total de cadenas cargadas: {len(cadenas_originales)}")
    
    if cadenas_originales and len(cadenas_originales) <= 10:
        print("\n📋 Cadenas cargadas:")
        mostrar_lista(cadenas_originales)


# ============================================================================
# FUNCIONES DE VISUALIZACIÓN
# ============================================================================

def mostrar_lista(lista):
    """
    Muestra una lista numerada de cadenas.
    
    Args:
        lista (list): Lista de strings a mostrar
    """
    for i, cadena in enumerate(lista[:10], 1):
        print(f"  {i}. {cadena}")


def mostrar_resultados_codificacion():
    """
    Muestra los resultados de la codificación en formato tabular.
    """
    print("="*60)
    print("RESULTADOS DE CODIFICACIÓN")
    print("="*60)
    
    for i in range(len(cadenas_originales)):
        print(f"\nCadena {i+1}:")
        print(f"  Original:   {cadenas_originales[i]}")
        print(f"  Codificada: {cadenas_codificadas[i]}")
        
        # Mostrar metadata si existe
        if datos_metadata[i]['metadata']:
            print(f"  Reemplazos: {len(datos_metadata[i]['metadata'])}")


def mostrar_resultados_decodificacion(decodificadas):
    """
    Muestra los resultados de la decodificación con verificación de integridad.
    
    Args:
        decodificadas (list): Lista de cadenas decodificadas
    """
    print("="*60)
    print("RESULTADOS DE DECODIFICACIÓN")
    print("="*60)
    
    for i in range(len(decodificadas)):
        print(f"\nCadena {i+1}:")
        print(f"  Codificada:   {cadenas_codificadas[i]}")
        print(f"  Decodificada: {decodificadas[i]}")
        
        # Verificar integridad
        if decodificadas[i] == cadenas_originales[i]:
            print("  Estado: ✓ OK (coincide con original)")
        else:
            print("  Estado: ✗ ERROR (no coincide)")


def guardar_archivo(nombre, datos1, datos2, tipo):
    """
    Guarda resultados en un archivo de texto.
    
    Args:
        nombre (str): Nombre del archivo de salida
        datos1 (list): Lista principal de resultados
        datos2 (list): Lista de referencia (originales o codificadas)
        tipo (str): Tipo de proceso ("codificación" o "decodificación")
    """
    try:
        with open(nombre, 'w', encoding='utf-8') as archivo:
            archivo.write(f"RESULTADOS DE {tipo.upper()}\n")
            archivo.write("="*60 + "\n\n")
            
            for i in range(len(datos1)):
                archivo.write(f"Cadena {i+1}:\n")
                if tipo == "codificación":
                    archivo.write(f"Original:   {datos2[i]}\n")
                    archivo.write(f"Codificada: {datos1[i]}\n")
                else:
                    archivo.write(f"Codificada:   {datos2[i]}\n")
                    archivo.write(f"Decodificada: {datos1[i]}\n")
                archivo.write("\n")
        
        print(f"💾 Resultados guardados en: {nombre}")
    except Exception as e:
        print(f"❌ Error al guardar el archivo: {e}")


# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

def mostrar_menu():
    """
    Muestra el menú principal del programa.
    """
    print("\n" + "="*50)
    print("   CODIFICADOR/DECODIFICADOR")
    print("   DE CADENAS NUMÉRICAS")
    print("="*50)
    print("1. Cargar datos")
    print("2. Codificar cadenas")
    print("3. Decodificar cadenas")
    print("4. Salir")
    print("-"*50)


def main():
    """
    Función principal que gestiona el flujo del programa.
    """
    print("\n🚀 Bienvenido al Codificador/Decodificador de Cadenas Numéricas")
    
    while True:
        mostrar_menu()
        
        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            print("\n❌ Por favor, ingrese un número válido.")
            continue
        
        if opcion == 1:
            cargar_datos()
        elif opcion == 2:
            procesar_codificacion()
        elif opcion == 3:
            procesar_decodificacion()
        elif opcion == 4:
            print("\n👋 ¡Hasta luego! Gracias por usar el programa.")
            break
        else:
            print("\n❌ Opción inválida. Por favor, seleccione una opción del 1 al 4.")


if __name__ == "__main__":
    main()
