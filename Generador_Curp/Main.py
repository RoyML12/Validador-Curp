import pandas as pd
import re
from datetime import datetime

# Función para cargar los datos del archivo Excel
def cargar_datos(ruta_archivo):
    return pd.read_excel(ruta_archivo, dtype=str)

# Función para generar una CURP a partir de los datos de entrada
def generar_curp(nombre, primer_apellido, segundo_apellido, fecha_nac, sexo, entidad):
    curp = (primer_apellido[0] +
            next((letra for letra in primer_apellido[1:] if letra in 'AEIOU'), 'X') +
            segundo_apellido[0] +
            nombre[0])
    curp += fecha_nac.strftime('%y%m%d')
    curp += sexo
    curp += entidad
    # Aquí agregarías lógica para las siguientes consonantes y dígitos.
    curp += 'XX'
    return curp.upper()

# Función para verificar si la CURP ya existe en el archivo Excel
def verificar_curp_existente(datos, curp):
    return curp in datos['CURP'].values

# Ejemplo de uso
def main():
    ruta_archivo = 'CURPs_Chiapas.xlsx'
    datos = cargar_datos(ruta_archivo)

    # Pedir datos al usuario
    nombre = input('Introduce tu nombre: ').upper()
    primer_apellido = input('Introduce tu primer apellido: ').upper()
    segundo_apellido = input('Introduce tu segundo apellido: ').upper()
    fecha_nac = datetime.strptime(input('Introduce tu fecha de nacimiento (dd/mm/aaaa): '), '%d/%m/%Y')
    sexo = input('Introduce el sexo (H/M): ').upper()
    entidad = input('Introduce la entidad de nacimiento (clave de dos letras): ').upper()
    
    # Generar la CURP
    curp_generada = generar_curp(nombre, primer_apellido, segundo_apellido, fecha_nac, sexo, entidad)
    
    # Verificar si la CURP ya existe
    if verificar_curp_existente(datos, curp_generada):
        print('La CURP generada ya existe en la base de datos.')
    else:
        print('La CURP generada es:', curp_generada)
        # Aquí podrías añadir la nueva CURP a tu archivo Excel si es necesario

if __name__ == '__main__':
    main()
