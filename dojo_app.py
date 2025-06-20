from tkinter import Tk, Label, Entry, Button, messagebox, Frame
from datetime import date

alumnos = {}
ventas = []
donaciones = []

def registrar_alumno():
    nombre = entry_nombre.get()
    correo = entry_correo.get()
    if correo in alumnos:
        messagebox.showwarning("Aviso", "El alumno ya está registrado.")
    else:
        alumnos[correo] = {"nombre": nombre, "ventas": [], "monto": 0}
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
        venta = {"producto": producto, "cantidad": cantidad, "monto": monto, "fecha": str(date.today())}
        alumnos[correo]["ventas"].append(venta)
        alumnos[correo]["monto"] += monto
        ventas.append(venta)
        messagebox.showinfo("Éxito", "Venta registrada.")
    else:
        messagebox.showerror("Error", "Alumno no encontrado.")

def registrar_donacion():
    nombre = entry_donante_nombre.get()
    correo = entry_donante_correo.get()
    try:
        monto = float(entry_donante_monto.get())
    except ValueError:
        messagebox.showerror("Error", "Monto debe ser numérico.")
        return
    donacion = {"nombre": nombre, "correo": correo, "monto": monto, "fecha": str(date.today())}
    donaciones.append(donacion)
    messagebox.showinfo("Gracias", "Donación registrada.")

def ver_progreso():
    progreso = ""
    for correo, data in alumnos.items():
        progreso += f"{data['nombre']}: ${data['monto']:.2f}\n"
    messagebox.showinfo("Progreso de Recaudación", progreso if progreso else "Sin datos.")

ventana = Tk()
ventana.title("Dojo Recaudación")
ventana.geometry("900x680")  # Ajustado a tu pantalla
ventana.config(bg="#f0f4ff")

Label(ventana, text="🥋 Sistema de Apoyo para Torneos", bg="#f0f4ff", font=("Helvetica", 14, "bold")).pack(pady=5)

# Sección: Registro de Alumno
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

# Sección: Registro de Venta
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

# Sección: Donación
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

# Botón Ver Progreso
Button(ventana, text="📈 Ver Progreso de Recaudación", command=ver_progreso, bg="#bfdbfe", font=("Arial", 11)).pack(pady=10)

ventana.mainloop()
