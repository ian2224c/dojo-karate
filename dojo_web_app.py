from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from datetime import date

app = Flask(__name__)

# Archivos CSV
ARCHIVO_ALUMNOS = "alumnos.csv"
ARCHIVO_VENTAS = "ventas.csv"
ARCHIVO_DONACIONES = "donaciones.csv"

# Helpers para escribir datos en CSV
def guardar_alumno(correo, nombre, monto):
    existe = os.path.exists(ARCHIVO_ALUMNOS)
    with open(ARCHIVO_ALUMNOS, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["correo", "nombre", "monto"])
        if not existe:
            writer.writeheader()
        writer.writerow({"correo": correo, "nombre": nombre, "monto": monto})

def guardar_venta(correo, producto, cantidad, monto):
    existe = os.path.exists(ARCHIVO_VENTAS)
    with open(ARCHIVO_VENTAS, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["correo", "producto", "cantidad", "monto", "fecha"])
        if not existe:
            writer.writeheader()
        writer.writerow({"correo": correo, "producto": producto, "cantidad": cantidad, "monto": monto, "fecha": str(date.today())})

def guardar_donacion(nombre, correo, monto):
    existe = os.path.exists(ARCHIVO_DONACIONES)
    with open(ARCHIVO_DONACIONES, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["nombre", "correo", "monto", "fecha"])
        if not existe:
            writer.writeheader()
        writer.writerow({"nombre": nombre, "correo": correo, "monto": monto, "fecha": str(date.today())})

# Rutas
@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/registrar_alumno', methods=['GET', 'POST'])
def registrar_alumno():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        guardar_alumno(correo, nombre, 0)
        return redirect(url_for('inicio'))
    return render_template('registrar_alumno.html')

@app.route('/registrar_venta', methods=['GET', 'POST'])
def registrar_venta():
    if request.method == 'POST':
        correo = request.form['correo']
        producto = request.form['producto']
        cantidad = int(request.form['cantidad'])
        monto = float(request.form['monto'])
        guardar_venta(correo, producto, cantidad, monto)
        return redirect(url_for('inicio'))
    return render_template('registrar_venta.html')

@app.route('/registrar_donacion', methods=['GET', 'POST'])
def registrar_donacion():
    if request.method == 'POST':
        nombre = request.form['nombre']
        correo = request.form['correo']
        monto = float(request.form['monto'])
        guardar_donacion(nombre, correo, monto)
        return redirect(url_for('inicio'))
    return render_template('registrar_donacion.html')

@app.route('/progreso')
def progreso():
    datos = {}
    if os.path.exists(ARCHIVO_ALUMNOS):
        with open(ARCHIVO_ALUMNOS, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                datos[row['nombre']] = float(row['monto'])
    return render_template('progreso.html', datos=datos)

if __name__ == '__main__':
    app.run(debug=True)
