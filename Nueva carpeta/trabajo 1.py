import tkinter as tk
from tkinter import messagebox

# --- CLASES DE LÓGICA (POO) ---
# -----------------------------------------------------------
# CLASE USUARIO
# Se encarga de validar el acceso al sistema
# -----------------------------------------------------------

class Usuario:
    """Clase para gestionar el acceso al sistema"""
    def __init__(self):
        # Atributos privados con las credenciales exactas solicitadas
        self._usuario = "programacion"
        self._password = "programacion"

    def validar(self, usuario_ingresado, password_ingresada):
        """Valida si las credenciales coinciden con las almacenadas"""
        return self._usuario == usuario_ingresado and self._password == password_ingresada
    
# -----------------------------------------------------------
# CLASE COMPUTADOR
# Representa un computador que entra a mantenimiento
# -----------------------------------------------------------
class ComputadorMantenimiento:
    """Clase que representa un computador en revisión"""
    def __init__(self, codigo, valor_hora):
        # Atributos privados para encapsular la información del equipo
        self._codigo = codigo
        self._hora_entrada = 0
        self._valor_hora = valor_hora

    def registrar_entrada(self, hora):
        """Asigna la hora de inicio del mantenimiento"""
        self._hora_entrada = hora

    def calcular_valor(self, hora_salida):
        """Calcula el costo total basado en el tiempo transcurrido"""
        duracion = hora_salida - self._hora_entrada
        return duracion * self._valor_hora

    def obtener_codigo(self):
        """Método Getter para obtener el código del atributo privado"""
        return self._codigo

# --- APLICACIÓN DE INTERFAZ GRÁFICA (GUI) ---
# -----------------------------------------------------------
# CLASE PRINCIPAL DE LA APLICACIÓN
# Maneja la interfaz gráfica del sistema
# -----------------------------------------------------------

class MaintenanceApp:
    """Clase principal que gestiona la interfaz gráfica y la lógica del negocio"""
    def __init__(self, root):
        self.root = root
        self.root.title("Technical Support System")
        self.root.geometry("450x600")
        
        # Lista interna para almacenar los objetos de tipo ComputadorMantenimiento
        self.pc_list = []  
        self.auth = Usuario()
        self.login_interface()
# -------------------------------------------------------
    # PANTALLA DE LOGIN
    # -------------------------------------------------------
    def login_interface(self):
        """Crea y muestra la pantalla de inicio de sesión"""
        self.frame = tk.Frame(self.root, pady=20)
        self.frame.pack()

        tk.Label(self.frame, text="USERNAME:").pack()
        self.ent_user = tk.Entry(self.frame)
        self.ent_user.pack()

        tk.Label(self.frame, text="PASSWORD:").pack()
        self.ent_pass = tk.Entry(self.frame, show="*")
        self.ent_pass.pack()

        tk.Button(self.frame, text="LOGIN", command=self.check_login).pack(pady=10)
# -------------------------------------------------------
    # VALIDACIÓN DE LOGIN
    # -------------------------------------------------------
    def check_login(self):
        """Valida el acceso del usuario antes de entrar al sistema principal"""
        if self.auth.validar(self.ent_user.get(), self.ent_pass.get()):
            self.frame.destroy()
            self.main_system()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")
# -------------------------------------------------------
    # INTERFAZ PRINCIPAL DEL SISTEMA
    # -------------------------------------------------------
    def main_system(self):
        """Crea la interfaz principal del sistema de mantenimiento"""
        self.main_frame = tk.Frame(self.root, padx=20, pady=10)
        self.main_frame.pack()

        # SECCIÓN DE REGISTRO
        tk.Label(self.main_frame, text="--- PC REGISTRATION ---", font=("Arial", 10, "bold")).pack()
        tk.Label(self.main_frame, text="PC Code:").pack()
        self.code_entry = tk.Entry(self.main_frame); self.code_entry.pack()

        tk.Label(self.main_frame, text="Entry Hour (24h):").pack()
        self.in_entry = tk.Entry(self.main_frame); self.in_entry.pack()

        tk.Label(self.main_frame, text="Price per Hour:").pack()
        self.rate_entry = tk.Entry(self.main_frame); self.rate_entry.pack()

        tk.Button(self.main_frame, text="Register Entry", command=self.add_pc).pack(pady=10)

        # SECCIÓN DE VISUALIZACIÓN (Lista visible solicitada)
        tk.Label(self.main_frame, text="--- REGISTERED COMPUTERS ---", font=("Arial", 10, "bold")).pack()
        self.listbox_pcs = tk.Listbox(self.main_frame, width=40, height=5)
        self.listbox_pcs.pack(pady=5)

        # SECCIÓN DE SALIDA
        tk.Label(self.main_frame, text="--- PROCESS EXIT ---", font=("Arial", 10, "bold")).pack()
        tk.Label(self.main_frame, text="Exit Hour:").pack()
        self.out_entry = tk.Entry(self.main_frame); self.out_entry.pack()

        tk.Button(self.main_frame, text="Calculate and Checkout Selected PC", command=self.process_exit).pack(pady=5)

    # GUARDAR COMPUTADOR EN LA LISTA
    # -------------------------------------------------------
    def add_pc(self):
        """Instancia un nuevo objeto ComputadorMantenimiento y lo agrega a la lista y al Listbox"""
        try:
            code = self.code_entry.get()
            h_in = float(self.in_entry.get())
            rate = float(self.rate_entry.get())

            if not (0 <= h_in <= 23) or code == "":
                raise ValueError("Valid hour or code required")

            # Creación del objeto
            new_pc = ComputadorMantenimiento(code, rate)
            new_pc.registrar_entrada(h_in)
            
            # Guardar en la lista interna
            self.pc_list.append(new_pc)
            # Actualizar la lista visible en la interfaz
            self.listbox_pcs.insert(tk.END, f"Code: {code} | In: {h_in}")
            
            messagebox.showinfo("Success", f"PC {code} registered in system.")
            self.code_entry.delete(0, tk.END) # Limpiar campos
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter valid values (Code and Hours 0-23)")
 
    # PROCESAR SALIDA DEL COMPUTADOR SELECCIONADO
    # -------------------------------------------------------
    def process_exit(self):
        """Busca el PC seleccionado en la lista visual y procesa su salida"""
        # Verificar si hay una selección en el Listbox
        selection = self.listbox_pcs.curselection()
        if not selection:
            return messagebox.showwarning("Warning", "Please select a PC from the list.")

        try:
            h_out = float(self.out_entry.get())
            if not (0 <= h_out <= 23):
                raise ValueError("Hour range error")

            # Obtener el índice seleccionado y el objeto correspondiente
            index = selection[0]
            current_pc = self.pc_list[index]
            
            # Validar que la hora de salida sea lógica
            if h_out < current_pc._hora_entrada:
                return messagebox.showerror("Time Error", "Exit hour cannot be before entry hour.")

            # Calcular costo y mostrar reporte
            total = current_pc.calcular_valor(h_out)
            messagebox.showinfo("Final Report", 
                                f"PC Code: {current_pc.obtener_codigo()}\n"
                                f"Total Diagnosis Value: ${total:.2f}")

            # Eliminar el registro procesado de ambas listas
            self.pc_list.pop(index)
            self.listbox_pcs.delete(index)
            self.out_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a valid exit hour (0-23)")

if __name__ == "__main__":
    # Inicialización del bucle principal de la aplicación
    root = tk.Tk()
    app = MaintenanceApp(root)
    root.mainloop()