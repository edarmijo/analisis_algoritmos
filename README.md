# Proyecto: Codificador y Decodificador de Cadenas Numéricas

## Introducción

Este proyecto implementa un sistema para **codificar y decodificar cadenas numéricas** de forma eficiente y reversible.  
La codificación divide cada cadena en símbolos de ancho variable y reemplaza las repeticiones utilizando una búsqueda **bidireccional** del vecino numérico más cercano disponible.  
Durante este proceso se genera una **metadata** que registra cada reemplazo, permitiendo que la decodificación restaure con exactitud la cadena original.


##  Pseudocódigo de las Funciones Principales


###  Imagen 1 – Pseudocódigo de `codificar_cadena`
![pseudo1](https://github.com/user-attachments/assets/1d0aa5c1-2e31-4bc6-8e9b-d4582344f8fb)


###  Imagen 2 – Pseudocódigo de `procesar_codificacion`
![pseudo2](https://github.com/user-attachments/assets/c3dc84e1-3ca4-4f9c-b4c9-8d49f8a1d0c7)


###  Imagen 3 – Pseudocódigo de `procesar_decodificacion`
![pseudo3](https://github.com/user-attachments/assets/998c97f4-b1a1-4040-85bc-b02cbf64cd8e)


---

## 📝 Notas

- El algoritmo está diseñado para admitir cadenas de **longitud arbitraria** (10, 50, 100, 500 dígitos o más).
- Se garantiza que todo reemplazo realizado durante la codificación es reversible gracias a la metadata generada.
- El proyecto está estructurado de forma modular para facilitar mantenimiento y extensibilidad.

---
