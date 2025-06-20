import csv
import os
from tkinter import Tk, Label, Entry, Button, messagebox, Frame
from datetime import date

# Archivos CSV
ARCHIVO_ALUMNOS = "alumnos.csv"
ARCHIVO_VENTAS = "ventas.csv"
ARCHIVO_DONACIONES = "donaciones.csv"

# Estructuras en memoria
alumnos = {}
ventas = []
donaciones = []

# ------------------ Funciones de CSV ------------------

def cargar_datos():
    if os.path.exists(ARCHIVO_ALUMNOS):
        with open(ARCHIVO_ALUMNOS, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                alumnos[row['correo']] = {"nombre": row['nombre'], "ventas": [], "monto": float(row['monto'])}

    if os.path.exists(ARCHIVO_VENTAS):
        with open(ARCHIVO_VENTAS, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                venta = {
                    "producto": row["producto"],
                    "cantidad": int(row["cantidad"]),
                    "monto": float(row["monto"]),
                    "fecha": row["fecha"]
                }
                ventas.append(venta)
                correo = row["correo"]
                if correo in alumnos:
                    alumnos[correo]["ventas"].append(venta)

    if os.path.exists(ARCHIVO_DONACIONES):
        with open(ARCHIVO_DONACIONES, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                donaciones.append({
                    "nombre": row["nombre"],
                    "correo": row["correo"],
                    "monto": float(row["monto"]),
                    "fecha": row["fecha"]
                })

def guardar_alumno_csv(correo, nombre, monto):
    existe = os.path.exists(ARCHIVO_ALUMNOS)
    with open(ARCHIVO_ALUMNOS, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["correo", "nombre", "monto"])
        if not existe:
            writer.writeheader()
        writer.writerow({"correo": correo, "nombre": nombre, "monto": monto})

def guardar_venta_csv(correo, producto, cantidad, monto, fecha):
    existe = os.path.exists(ARCHIVO_VENTAS)
    with open(ARCHIVO_VENTAS, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["correo", "producto", "cantidad", "monto", "fecha"])
        if not existe:
            writer.writeheader()
        writer.writerow({"correo": correo, "producto": producto, "cantidad": cantidad, "monto": monto, "fecha": fecha})

def guardar_donacion_csv(nombre, correo, monto, fecha):
    existe = os.path.exists(ARCHIVO_DONACIONES)
    with open(ARCHIVO_DONACIONES, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["nombre", "correo", "monto", "fecha"])
        if not existe:
            writer.writeheader()
        writer.writerow({"nombre": nombre, "correo": correo, "monto": monto, "fecha": fecha})

# ------------------ Funciones GUI ------------------

def registrar_alumno():
    nombre = entry_nombre.get()
    correo = entry_correo.get()
    if correo in alumnos:
        messagebox.showwarning("Aviso", "El alumno ya está registrado.")
    else:
        alumnos[correo] = {"nombre": nombre, "ventas": [], "monto": 0}
        guardar_alumno_csv(correo, nombre, 0)
        messagebox.showinfo("Éxito", f"Alumno {nombre} registrado.")

def registrar_venta():
    correo = entry_venta_correo.get()
    producto = entry_producto.get()
    try:
        cantidad = int(entry_cantidad.get())
        monto = float(entry_monto.get())
    except ValueError:
        messagebox.showerror("Error", "Cantidad y monto deben ser numéricos.")
        return
    if correo in alumnos:
        fecha_actual = str(date.today())
        venta = {"producto": producto, "cantidad": cantidad, "monto": monto, "fecha": fecha_actual}
        alumnos[correo]["ventas"].append(venta)
        alumnos[correo]["monto"] += monto
        ventas.append(venta)
        guardar_venta_csv(correo, producto, cantidad, monto, fecha_actual)
        actualizar_csv_alumnos()
        messagebox.showinfo("Éxito", "Venta registrada.")
    else:
        messagebox.showerror("Error", "Alumno no encontrado.")

def actualizar_csv_alumnos():
    with open(ARCHIVO_ALUMNOS, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["correo", "nombre", "monto"])
        writer.writeheader()
        for correo, data in alumnos.items():
            writer.writerow({"correo": correo, "nombre": data["nombre"], "monto": data["monto"]})

def registrar_donacion():
    nombre = entry_donante_nombre.get()
    correo = entry_donante_correo.get()
    try:
        monto = float(entry_donante_monto.get())
    except ValueError:
        messagebox.showerror("Error", "Monto debe ser numérico.")
        return
    fecha_actual = str(date.today())
    donacion = {"nombre": nombre, "correo": correo, "monto": monto, "fecha": fecha_actual}
    donaciones.append(donacion)
    guardar_donacion_csv(nombre, correo, monto, fecha_actual)
    messagebox.showinfo("Gracias", "Donación registrada.")

def ver_progreso():
    progreso = ""
    for correo, data in alumnos.items():
        progreso += f"{data['nombre']}: ${data['monto']:.2f}\n"
    messagebox.showinfo("Progreso de Recaudación", progreso if progreso else "Sin datos.")

# ------------------ Interfaz ------------------

ventana = Tk()
ventana.title("Dojo Recaudación con CSV")
ventana.geometry("900x680")
ventana.config(bg="#f0f4ff")

Label(ventana, text="🥋 Sistema de Apoyo para Torneos", bg="#f0f4ff", font=("Helvetica", 14, "bold")).pack(pady=5)

# Registro alumno
frame_alumno = Frame(ventana, bg="#dceefb", bd=1, relief="groove", padx=10, pady=5)
frame_alumno.pack(pady=5, fill="x", padx=10)
Label(frame_alumno, text="👤 Registro de Alumno", bg="#dceefb", font=("Arial", 11, "bold")).pack()
Label(frame_alumno, text="Nombre:", bg="#dceefb").pack()
entry_nombre = Entry(frame_alumno)
entry_nombre.pack()
Label(frame_alumno, text="Correo:", bg="#dceefb").pack()
entry_correo = Entry(frame_alumno)
entry_correo.pack()
Button(frame_alumno, text="Registrar", command=registrar_alumno, bg="#a7f3d0").pack(pady=3)

# Registro venta
frame_venta = Frame(ventana, bg="#fff7ed", bd=1, relief="groove", padx=10, pady=5)
frame_venta.pack(pady=5, fill="x", padx=10)
Label(frame_venta, text="🛒 Registrar Venta", bg="#fff7ed", font=("Arial", 11, "bold")).pack()
Label(frame_venta, text="Correo del Alumno:", bg="#fff7ed").pack()
entry_venta_correo = Entry(frame_venta)
entry_venta_correo.pack()
Label(frame_venta, text="Producto:", bg="#fff7ed").pack()
entry_producto = Entry(frame_venta)
entry_producto.pack()
Label(frame_venta, text="Cantidad:", bg="#fff7ed").pack()
entry_cantidad = Entry(frame_venta)
entry_cantidad.pack()
Label(frame_venta, text="Monto Total:", bg="#fff7ed").pack()
entry_monto = Entry(frame_venta)
entry_monto.pack()
Button(frame_venta, text="Guardar Venta", command=registrar_venta, bg="#fdba74").pack(pady=3)

# Donación
frame_donacion = Frame(ventana, bg="#fef2f2", bd=1, relief="groove", padx=10, pady=5)
frame_donacion.pack(pady=5, fill="x", padx=10)
Label(frame_donacion, text="💰 Donación", bg="#fef2f2", font=("Arial", 11, "bold")).pack()
Label(frame_donacion, text="Nombre del Donante:", bg="#fef2f2").pack()
entry_donante_nombre = Entry(frame_donacion)
entry_donante_nombre.pack()
Label(frame_donacion, text="Correo:", bg="#fef2f2").pack()
entry_donante_correo = Entry(frame_donacion)
entry_donante_correo.pack()
Label(frame_donacion, text="Monto:", bg="#fef2f2").pack()
entry_donante_monto = Entry(frame_donacion)
entry_donante_monto.pack()
Button(frame_donacion, text="Donar", command=registrar_donacion, bg="#fca5a5").pack(pady=3)

Button(ventana, text="📈 Ver Progreso de Recaudación", command=ver_progreso, bg="#bfdbfe", font=("Arial", 11)).pack(pady=10)

# Cargar datos al iniciar
cargar_datos()
ventana.mainloop()
