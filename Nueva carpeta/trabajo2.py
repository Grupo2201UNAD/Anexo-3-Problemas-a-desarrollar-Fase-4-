import tkinter as tk
from tkinter import messagebox

# -----------------------------------------------------------
# CLASE USUARIO
# Se encarga de validar el acceso al sistema
# -----------------------------------------------------------
class Usuario:

    def __init__(self):
        # Credenciales solicitadas en la guía
        self._usuario = "programacion"
        self._password = "programacion"

    # Método que valida si el usuario y contraseña coinciden
    def validar(self, usuario_ingresado, password_ingresada):
        return self._usuario == usuario_ingresado and self._password == password_ingresada


# -----------------------------------------------------------
# CLASE COMPUTADOR
# Representa un computador que entra a mantenimiento
# -----------------------------------------------------------
class ComputadorMantenimiento:

    def __init__(self, codigo, valor_hora):
        # Atributos privados del objeto
        self._codigo = codigo
        self._hora_entrada = 0
        self._valor_hora = valor_hora

    # Método para registrar la hora de entrada
    def registrar_entrada(self, hora):
        self._hora_entrada = hora

    # Método para calcular el valor total del mantenimiento
    def calcular_valor(self, hora_salida):
        tiempo_total = hora_salida - self._hora_entrada
        return tiempo_total * self._valor_hora

    # Método para obtener el código del computador
    def obtener_codigo(self):
        return self._codigo


# -----------------------------------------------------------
# CLASE PRINCIPAL DE LA APLICACIÓN
# Maneja la interfaz gráfica del sistema
# -----------------------------------------------------------
class MaintenanceApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Technical Support Center")
        self.root.geometry("420x500")

        # Lista donde se almacenan los computadores registrados
        self.lista_computadores = []

        # Sistema de autenticación
        self.sistema_auth = Usuario()

        # Se muestra la pantalla de login
        self.pantalla_login()

    # -------------------------------------------------------
    # PANTALLA DE LOGIN
    # -------------------------------------------------------
    def pantalla_login(self):

        self.frame_login = tk.Frame(self.root, pady=20)
        self.frame_login.pack()

        tk.Label(self.frame_login, text="USERNAME").pack()

        self.entry_user = tk.Entry(self.frame_login)
        self.entry_user.pack()

        tk.Label(self.frame_login, text="PASSWORD").pack()

        self.entry_pass = tk.Entry(self.frame_login, show="*")
        self.entry_pass.pack()

        tk.Button(self.frame_login,
                  text="LOGIN",
                  command=self.ejecutar_login).pack(pady=10)

    # -------------------------------------------------------
    # VALIDACIÓN DE LOGIN
    # -------------------------------------------------------
    def ejecutar_login(self):

        usuario = self.entry_user.get()
        password = self.entry_pass.get()

        if self.sistema_auth.validar(usuario, password):

            self.frame_login.destroy()
            self.sistema_principal()

        else:

            messagebox.showerror("Error", "Invalid credentials")

    # -------------------------------------------------------
    # INTERFAZ PRINCIPAL DEL SISTEMA
    # -------------------------------------------------------
    def sistema_principal(self):

        self.frame_main = tk.Frame(self.root, padx=20, pady=10)
        self.frame_main.pack()

        # -------- REGISTRO DE COMPUTADORES --------
        tk.Label(self.frame_main,
                 text="--- PC REGISTRATION ---",
                 font=("Arial", 10, "bold")).pack()

        tk.Label(self.frame_main, text="PC Code").pack()
        self.ent_codigo = tk.Entry(self.frame_main)
        self.ent_codigo.pack()

        tk.Label(self.frame_main, text="Entry Hour").pack()
        self.ent_hora_in = tk.Entry(self.frame_main)
        self.ent_hora_in.pack()

        tk.Label(self.frame_main, text="Value per Hour").pack()
        self.ent_valor = tk.Entry(self.frame_main)
        self.ent_valor.pack()

        tk.Button(self.frame_main,
                  text="Register Entry",
                  command=self.guardar_computador).pack(pady=10)

        # -------- LISTA VISUAL DE COMPUTADORES --------
        tk.Label(self.frame_main,
                 text="Registered PCs",
                 font=("Arial", 10, "bold")).pack()

        # Listbox permite visualizar todos los registros
        self.lista_visual = tk.Listbox(self.frame_main, width=40)
        self.lista_visual.pack(pady=5)

        # -------- REGISTRO DE SALIDA --------
        tk.Label(self.frame_main,
                 text="--- CHECKOUT ---",
                 font=("Arial", 10, "bold")).pack()

        tk.Label(self.frame_main, text="Exit Hour").pack()
        self.ent_hora_out = tk.Entry(self.frame_main)
        self.ent_hora_out.pack()

        tk.Button(self.frame_main,
                  text="Process and Calculate",
                  command=self.procesar_salida).pack(pady=5)

    # -------------------------------------------------------
    # GUARDAR COMPUTADOR EN LA LISTA
    # -------------------------------------------------------
    def guardar_computador(self):

        try:

            codigo = self.ent_codigo.get()
            h_in = float(self.ent_hora_in.get())
            valor = float(self.ent_valor.get())

            # Validación de hora
            if not (0 <= h_in <= 23):
                raise ValueError()

            # Crear objeto computador
            pc = ComputadorMantenimiento(codigo, valor)

            # Registrar hora de entrada
            pc.registrar_entrada(h_in)

            # Guardar en la lista
            self.lista_computadores.append(pc)

            # Mostrar en la lista visual
            self.lista_visual.insert(tk.END, f"PC {codigo} - Entry {h_in}")

            messagebox.showinfo("Success", f"PC {codigo} registered")

        except ValueError:

            messagebox.showerror("Error", "Enter valid numeric data")

    # -------------------------------------------------------
    # PROCESAR SALIDA DEL COMPUTADOR SELECCIONADO
    # -------------------------------------------------------
    def procesar_salida(self):

        try:

            seleccion = self.lista_visual.curselection()

            # Verifica que se haya seleccionado un registro
            if not seleccion:
                messagebox.showwarning("Warning", "Select a PC from the list")
                return

            index = seleccion[0]

            h_out = float(self.ent_hora_out.get())

            if not (0 <= h_out <= 23):
                raise ValueError()

            pc = self.lista_computadores[index]

            if h_out < pc._hora_entrada:
                messagebox.showerror("Error", "Exit hour cannot be before entry hour")
                return

            costo = pc.calcular_valor(h_out)

            messagebox.showinfo(
                "Total Cost",
                f"PC: {pc.obtener_codigo()}\nTotal to pay: ${costo:.2f}"
            )

            # Eliminar de la lista después del cálculo
            self.lista_visual.delete(index)
            self.lista_computadores.pop(index)

        except ValueError:

            messagebox.showerror("Error", "Invalid exit hour")


# -----------------------------------------------------------
# PROGRAMA PRINCIPAL
# -----------------------------------------------------------
if __name__ == "__main__":

    root = tk.Tk()

    app = MaintenanceApp(root)

    # Bucle principal de la interfaz gráfica
    root.mainloop()