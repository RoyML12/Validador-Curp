from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
import string
import random

app = Flask(__name__)

# Ruta del archivo Excel
RUTA_ARCHIVO = 'CURPs_Chiapas.xlsx'

# Función para cargar los datos del archivo Excel
def cargar_datos():
    try:
        return pd.read_excel(RUTA_ARCHIVO, dtype=str)
    except FileNotFoundError:
        return pd.DataFrame(columns=['CURP'])

# Funciones auxiliares para la generación de la CURP
def primera_vocal_interna(cadena):
    for letra in cadena[1:]:
        if letra in 'AEIOU':
            return letra
    return 'X'

def primera_consonante_interna(cadena):
    for letra in cadena[1:]:
        if letra not in 'AEIOU':
            return letra
    return 'X'

# Función para buscar en el archivo Excel y encontrar una CURP que coincida con los primeros 16 caracteres
def obtener_homoclave_y_digito_verificador(curp_buscada, datos):
    coincidencias = datos[datos['CURP'].str.startswith(curp_buscada[:16], na=False)]
    if not coincidencias.empty:
        curp_completa = coincidencias.iloc[0]['CURP']
        return curp_completa[-2:]  # Retorna los últimos dos caracteres (homoclave y dígito verificador)
    return None

# Función para generar una CURP a partir de los datos de entrada, incluyendo homoclave y dígito verificador
def generar_curp(nombre, primer_apellido, segundo_apellido, fecha_nac, sexo, entidad, homoclave_y_digito=None):
    curp = (
        primer_apellido[0] +
        primera_vocal_interna(primer_apellido) +
        segundo_apellido[0] +
        nombre[0] +
        fecha_nac.strftime('%y%m%d') +
        sexo +
        entidad +
        primera_consonante_interna(primer_apellido) +
        primera_consonante_interna(segundo_apellido) +
        primera_consonante_interna(nombre)
    )

    # Añadir la homoclave y el dígito verificador si se proporcionan
    curp += homoclave_y_digito if homoclave_y_digito else 'XX'

    return curp.upper()

# Endpoint para generar y verificar una CURP
@app.route('/curp', methods=['POST'])
def curp_endpoint():
    # Obtiene los datos del cuerpo de la solicitud JSON
    data = request.json
    nombre = data['nombre'].upper()
    primer_apellido = data['primer_apellido'].upper()
    segundo_apellido = data['segundo_apellido'].upper()
    fecha_nac = datetime.strptime(data['fecha_nac'], '%d/%m/%Y')
    sexo = data['sexo'].upper()
    entidad = data['entidad'].upper()

    # Carga los datos del archivo Excel
    datos = cargar_datos()

    # Genera los primeros 16 caracteres de la CURP
    curp_sin_homoclave = generar_curp(nombre, primer_apellido, segundo_apellido, fecha_nac, sexo, entidad)[:16]

    # Busca la homoclave y el dígito verificador en el archivo Excel
    homoclave_y_digito = obtener_homoclave_y_digito_verificador(curp_sin_homoclave, datos)

    # Genera la CURP completa con homoclave y dígito verificador
    curp_completa = generar_curp(nombre, primer_apellido, segundo_apellido, fecha_nac, sexo, entidad, homoclave_y_digito)

    # Devuelve la CURP completa
    return jsonify({'curp': curp_completa}), 200

if __name__ == '__main__':
    app.run(debug=True)
