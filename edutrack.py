import tkinter as tk
from tkinter import ttk, messagebox

# Simulación simple de usuarios para login
USUARIOS = {
    "estudiante@cetis1.mx": "password123",
    "docente@cetis1.mx": "docente456"
}

class EduTrackApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("EduTrack CETis 1")
        self.geometry("600x400")
        self.resizable(False, False)
        
        self.usuario_actual = None
        
        self.login_frame = LoginFrame(self, self.login_exitoso)
        self.dashboard_frame = None
        
        self.login_frame.pack(fill="both", expand=True)
    
    def login_exitoso(self, usuario):
        self.usuario_actual = usuario
        self.login_frame.pack_forget()
        self.dashboard_frame = DashboardFrame(self, self.usuario_actual)
        self.dashboard_frame.pack(fill="both", expand=True)

class LoginFrame(tk.Frame):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.on_login_success = on_login_success
        
        tk.Label(self, text="EduTrack CETis 1", font=("Arial", 24)).pack(pady=20)
        
        self.email_var = tk.StringVar()
        self.pass_var = tk.StringVar()
        
        tk.Label(self, text="Correo:").pack(anchor="w", padx=100)
        tk.Entry(self, textvariable=self.email_var, width=40).pack(padx=100)
        
        tk.Label(self, text="Contraseña:").pack(anchor="w", padx=100, pady=(10,0))
        tk.Entry(self, textvariable=self.pass_var, show="*", width=40).pack(padx=100)
        
        tk.Button(self, text="Iniciar Sesión", command=self.validar_login).pack(pady=20)
    
    def validar_login(self):
        email = self.email_var.get()
        password = self.pass_var.get()
        if email in USUARIOS and USUARIOS[email] == password:
            self.on_login_success(email)
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

class DashboardFrame(tk.Frame):
    def __init__(self, parent, usuario):
        super().__init__(parent)
        self.usuario = usuario
        
        # Crear pestañas
        self.tabControl = ttk.Notebook(self)
        
        self.tab_dashboard = ttk.Frame(self.tabControl)
        self.tab_agenda = ttk.Frame(self.tabControl)
        self.tab_calificaciones = ttk.Frame(self.tabControl)
        self.tab_mensajes = ttk.Frame(self.tabControl)
        self.tab_perfil = ttk.Frame(self.tabControl)
        
        self.tabControl.add(self.tab_dashboard, text='Inicio')
        self.tabControl.add(self.tab_agenda, text='Agenda')
        self.tabControl.add(self.tab_calificaciones, text='Calificaciones')
        self.tabControl.add(self.tab_mensajes, text='Mensajes')
        self.tabControl.add(self.tab_perfil, text='Perfil')
        
        self.tabControl.pack(expand=1, fill="both")
        
        self.crear_dashboard()
        self.crear_agenda()
        self.crear_calificaciones()
        self.crear_mensajes()
        self.crear_perfil()
    
    def crear_dashboard(self):
        lbl = tk.Label(self.tab_dashboard, text=f"Bienvenido {self.usuario}", font=("Arial", 18))
        lbl.pack(pady=20)
        
        # Aquí se podrían mostrar resumenes, alertas, etc.
        resumen = tk.Label(self.tab_dashboard, text="Promedio General: 8.5\nMaterias en Riesgo: 1\nTareas próximas: 2", font=("Arial", 14))
        resumen.pack(pady=10)
    
    def crear_agenda(self):
        tk.Label(self.tab_agenda, text="Lista de tareas próximas", font=("Arial", 16)).pack(pady=10)
        # Lista simple de ejemplo
        tareas = ["Matemáticas - Entregar ejercicio 5 (15/06)", 
                  "Historia - Investigar revolución (17/06)"]
        for tarea in tareas:
            tk.Label(self.tab_agenda, text=f"• {tarea}", font=("Arial", 12)).pack(anchor="w", padx=20)
    
    def crear_calificaciones(self):
        tk.Label(self.tab_calificaciones, text="Calificaciones por materia", font=("Arial", 16)).pack(pady=10)
        califs = {
            "Matemáticas": 7.5,
            "Historia": 8.8,
            "Física": 6.2
        }
        for materia, calif in califs.items():
            color = "red" if calif < 7 else "green"
            lbl = tk.Label(self.tab_calificaciones, text=f"{materia}: {calif}", font=("Arial", 12), fg=color)
            lbl.pack(anchor="w", padx=20)
    
    def crear_mensajes(self):
        tk.Label(self.tab_mensajes, text="Mensajes de docentes", font=("Arial", 16)).pack(pady=10)
        mensajes = [
            "Profe Juan: No olviden entregar la tarea de matemáticas el viernes.",
            "Profe Ana: Examen de historia será la próxima semana."
        ]
        for msg in mensajes:
            tk.Label(self.tab_mensajes, text=f"• {msg}", font=("Arial", 12)).pack(anchor="w", padx=20)
    
    def crear_perfil(self):
        tk.Label(self.tab_perfil, text="Perfil de usuario", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.tab_perfil, text=f"Correo: {self.usuario}", font=("Arial", 12)).pack(pady=5)
        tk.Button(self.tab_perfil, text="Cerrar sesión", command=self.cerrar_sesion).pack(pady=20)
    
    def cerrar_sesion(self):
        self.master.dashboard_frame.pack_forget()
        self.master.usuario_actual = None
        self.master.login_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = EduTrackApp()
    app.mainloop()
