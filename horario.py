from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Cargar el archivo Excel y convertirlo en un DataFrame
def cargar_horario(nombre_archivo):
    return pd.read_excel(nombre_archivo)

# Guardar el horario modificado en un archivo Excel
def guardar_horario(horario, nombre_archivo):
    horario.to_excel(nombre_archivo, index=False)

# Función para modificar el horario
def modificar_horario(horario, id_clase, dia, hora, nueva_clase, nuevo_profesor, nueva_sala):
    horario.loc[horario['id'] == id_clase, 'Dia'] = dia
    horario.loc[horario['id'] == id_clase, 'Hora'] = hora
    horario.loc[horario['id'] == id_clase, 'Clase'] = nueva_clase
    horario.loc[horario['id'] == id_clase, 'Profesor'] = nuevo_profesor
    horario.loc[horario['id'] == id_clase, 'Sala'] = nueva_sala

# Cargar el horario desde un archivo Excel
horario = cargar_horario('horario.xlsx')

# Ruta principal de la aplicación
@app.route('/', methods=['GET', 'POST'])
def horario():
    # Si se envió un formulario de modificación, procesarlo
    if request.method == 'POST':
        id_clase = request.form['id']
        dia = request.form['dia']
        hora = request.form['hora']
        nueva_clase = request.form['clase']
        nuevo_profesor = request.form['profesor']
        nueva_sala = request.form['sala']
        modificar_horario(horario, id_clase, dia, hora, nueva_clase, nuevo_profesor, nueva_sala)
        guardar_horario(horario, 'horario.xlsx')

    # Obtener los parámetros de búsqueda
    nombre_alumno = request.args.get('alumno', default='', type=str)
    nombre_profesor = request.args.get('profesor', default='', type=str)
    salas_disponibles = request.args.get('salas', default='', type=str).split(',')

    # Generar el horario para el alumno, profesor y salas disponibles
    horario_alumno = horario[(horario['Clase'].str.contains(nombre_alumno, case=False)) | (horario['Profesor'].str.contains(nombre_profesor, case=False)) | (horario['Sala'].isin(salas_disponibles))]

    # Convertir el DataFrame del horario en un diccionario que se puede pasar a la plantilla HTML
    horario_dict = horario_alumno.to_dict(orient='records')

    # Renderizar la plantilla HTML con el horario y los parámetros
