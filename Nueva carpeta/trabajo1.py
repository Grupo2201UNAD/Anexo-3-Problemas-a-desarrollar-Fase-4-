import tkinter as tk
from tkinter import messagebox, ttk

# ==========================================
# 1. CLASES DE LÓGICA (PROGRAMACIÓN ORIENTADA A OBJETOS)
# ==========================================

class Usuario:
    """Clase para gestionar el acceso de seguridad al sistema"""
    def __init__(self):
        self._usuario = "programacion"
        self._password = "programacion"

    def validar(self, u, p):
        return self._usuario == u and self._password == p

class Bonificable:
    """Mixin para gestionar bonos extra (Herencia Múltiple)"""
    def __init__(self):
        self._bonificaciones_extra = 0

    def agregar_bonificacion(self, monto):
        self._bonificaciones_extra += monto

class Empleado:
    """Clase base con método virtual y sobrecarga de información"""
    def __init__(self, nombre, identificacion, salario_base):
        self.nombre = nombre
        self.identificacion = identificacion
        self.salario_base = salario_base

    def calcular_salario(self):
        return self.salario_base

    def mostrar_informacion(self, salary=True):
        info = f"ID: {self.identificacion} | Name: {self.nombre}"
        if salary:
            info += f" | Total: ${self.calcular_salario():.2f}"
        return info

class EmpleadoTiempoCompletoBonificado(Empleado, Bonificable):
    def __init__(self, nombre, identificacion, salario_base, bono_fijo):
        Empleado.__init__(self, nombre, identificacion, salario_base)
        Bonificable.__init__(self)
        self.bono_fijo = bono_fijo

    def calcular_salario(self):
        return self.salario_base + self.bono_fijo + self._bonificaciones_extra

class EmpleadoPorHoras(Empleado):
    def __init__(self, nombre, identificacion, pago_hora, horas):
        super().__init__(nombre, identificacion, pago_hora)
        self.horas = horas

    def calcular_salario(self):
        return self.salario_base * self.horas

class ComputadorMantenimiento:
    def __init__(self, codigo, valor_hora):
        self._codigo = codigo
        self._hora_entrada = 0
        self._valor_hora = valor_hora

    def registrar_entrada(self, hora):
        self._hora_entrada = hora

    def calcular_valor(self, hora_salida):
        return (hora_salida - self._hora_entrada) * self._valor_hora

    def obtener_codigo(self):
        return self._codigo

# ==========================================
# 2. INTERFAZ GRÁFICA OPTIMIZADA
# ==========================================

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UNAD - Robust Management System")
        self.root.geometry("550x700")
        
        self.auth = Usuario()
        self.payroll_list = []
        self.maint_list = []
        
        self.login_ui()

    def login_ui(self):
        self.frame_login = tk.Frame(self.root, pady=50)
        self.frame_login.pack()
        tk.Label(self.frame_login, text="SYSTEM LOGIN", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(self.frame_login, text="Username:").pack()
        self.ent_user = tk.Entry(self.frame_login); self.ent_user.pack()
        tk.Label(self.frame_login, text="Password:").pack()
        self.ent_pass = tk.Entry(self.frame_login, show="*"); self.ent_pass.pack()
        tk.Button(self.frame_login, text="ENTER", command=self.check_auth, bg="navy", fg="white", width=15).pack(pady=20)

    def check_auth(self):
        if self.auth.validar(self.ent_user.get(), self.ent_pass.get()):
            self.frame_login.destroy()
            self.main_menu_ui()
        else:
            messagebox.showerror("Access Error", "Invalid Username or Password")

    def main_menu_ui(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab3 = tk.Frame(self.notebook, padx=15, pady=15)
        self.tab4 = tk.Frame(self.notebook, padx=15, pady=15)
        self.notebook.add(self.tab3, text="EXERCISE 3: PAYROLL")
        self.notebook.add(self.tab4, text="EXERCISE 4: MAINTENANCE")
        
        self.setup_payroll_ui()
        self.setup_maintenance_ui()

    def setup_payroll_ui(self):
        fields = [("Name:", "pay_name"), ("Base Salary/Rate:", "pay_base"), ("Extra (Bonus/Hours):", "pay_extra")]
        self.pay_entries = {}
        for text, var in fields:
            tk.Label(self.tab3, text=text).pack()
            ent = tk.Entry(self.tab3)
            ent.pack(); self.pay_entries[var] = ent

        self.pay_type = ttk.Combobox(self.tab3, values=["Full-Time", "Hourly"], state="readonly")
        self.pay_type.current(0); self.pay_type.pack(pady=10)

        tk.Button(self.tab3, text="Add Employee", command=self.add_to_payroll, bg="#e1e1e1").pack()
        self.pay_listbox = tk.Listbox(self.tab3, width=60, height=8)
        self.pay_listbox.pack(pady=15)
        tk.Button(self.tab3, text="Calculate Total Payroll", command=self.total_payroll, bg="green", fg="white").pack(fill=tk.X)

    def add_to_payroll(self):
        try:
            name = self.pay_entries["pay_name"].get()
            base = float(self.pay_entries["pay_base"].get())
            extra = float(self.pay_entries["pay_extra"].get())
            
            if not name: raise ValueError("Name is required")

            if self.pay_type.get() == "Full-Time":
                emp = EmpleadoTiempoCompletoBonificado(name, f"FT-{len(self.payroll_list)+1}", base, extra)
                emp.agregar_bonificacion(100)
            else:
                emp = EmpleadoPorHoras(name, f"H-{len(self.payroll_list)+1}", base, extra)
            
            self.payroll_list.append(emp)
            self.pay_listbox.insert(tk.END, emp.mostrar_informacion())
            for entry in self.pay_entries.values(): entry.delete(0, tk.END)
            
        except ValueError as e:
            messagebox.showerror("Input Error", f"Invalid data: {e}" if str(e) else "Please enter numeric values")

    def total_payroll(self):
        if not self.payroll_list:
            return messagebox.showwarning("Empty", "No employees registered yet.")
        total = sum(emp.calcular_salario() for emp in self.payroll_list)
        messagebox.showinfo("Payroll Result", f"Total Monthly Payroll: ${total:.2f}")

    def setup_maintenance_ui(self):
        tk.Label(self.tab4, text="PC Code:").pack()
        self.m_code = tk.Entry(self.tab4); self.m_code.pack()
        tk.Label(self.tab4, text="Entry Hour (0-23):").pack()
        self.m_in = tk.Entry(self.tab4); self.m_in.pack()
        tk.Label(self.tab4, text="Rate per Hour:").pack()
        self.m_rate = tk.Entry(self.tab4); self.m_rate.pack()

        tk.Button(self.tab4, text="Register PC", command=self.reg_maint).pack(pady=10)
        self.m_listbox = tk.Listbox(self.tab4, width=60, height=8)
        self.m_listbox.pack(pady=10)

        tk.Label(self.tab4, text="Exit Hour (0-23):").pack()
        self.m_out = tk.Entry(self.tab4); self.m_out.pack()
        tk.Button(self.tab4, text="Checkout Selected PC", command=self.checkout_maint, bg="orange").pack(pady=10, fill=tk.X)

    def reg_maint(self):
        try:
            c = self.m_code.get()
            h = float(self.m_in.get())
            r = float(self.m_rate.get())
            if not (0 <= h <= 23) or not c: raise ValueError("Check Code or Hour (0-23)")
            
            pc = ComputadorMantenimiento(c, r)
            pc.registrar_entrada(h)
            self.maint_list.append(pc)
            self.m_listbox.insert(tk.END, f"DEVICE: {c} | Registered at: {h}:00")
            self.m_code.delete(0, tk.END); self.m_in.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e) if str(e) else "Invalid numeric input")

    def checkout_maint(self):
        selection = self.m_listbox.curselection()
        if not selection:
            return messagebox.showwarning("Selection", "Please select a PC from the list first.")
        
        try:
            h_out = float(self.m_out.get())
            index = selection
            pc = self.maint_list[index]
            
            if not (0 <= h_out <= 23) or h_out < pc._hora_entrada:
                raise ValueError("Exit hour must be between 0-23 and after entry hour.")
            
            total = pc.calcular_valor(h_out)
            messagebox.showinfo("Invoice", f"PC Code: {pc.obtener_codigo()}\nTotal Cost: ${total:.2f}")
            self.maint_list.pop(index)
            self.m_listbox.delete(index)
            self.m_out.delete(0, tk.END)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except IndexError:
            messagebox.showerror("Error", "Selected item not found")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()