# Anexo-3-Problemas-a-desarrollar-Fase-4-
Anexo 3 – Problemas a desarrollar (Fase 4), Trabajo grupal 
"""
Sistema Integral - UNAD Fase 4
Gestión de Clientes, Servicios y Reservas
"""

from abc import ABC, abstractmethod
from datetime import datetime


# ===================== LOGS =====================
def registrar_log(mensaje):
    with open("logs.txt", "a") as archivo:
        archivo.write(f"{datetime.now()} - {mensaje}\n")


# ===================== EXCEPCIONES =====================
class ErrorSistema(Exception):
    pass


class ErrorValidacion(ErrorSistema):
    pass


class ErrorReserva(ErrorSistema):
    pass


# ===================== CLASE ABSTRACTA =====================
class Entidad(ABC):
    def __init__(self, id):
        self._id = id

    @abstractmethod
    def mostrar(self):
        pass


# ===================== CLIENTE =====================
class Cliente(Entidad):
    def __init__(self, id, nombre):
        super().__init__(id)
        self.nombre = nombre

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or valor.strip() == "":
            raise ErrorValidacion("Nombre inválido")
        self._nombre = valor

    def mostrar(self):
        return f"Cliente: {self._nombre}"


# ===================== SERVICIO ABSTRACTO =====================
class Servicio(ABC):
    def __init__(self, nombre, precio_base):
        if precio_base <= 0:
            raise ErrorValidacion("Precio inválido")
        self.nombre = nombre
        self.precio_base = precio_base

    @abstractmethod
    def calcular_costo(self):
        pass

    @abstractmethod
    def descripcion(self):
        pass


# ===================== SERVICIOS =====================
class ReservaSala(Servicio):
    def calcular_costo(self, horas=1):
        if horas <= 0:
            raise ErrorValidacion("Horas inválidas")
        return self.precio_base * horas

    def descripcion(self):
        return "Reserva de sala"


class AlquilerEquipo(Servicio):
    def calcular_costo(self, dias=1):
        if dias <= 0:
            raise ErrorValidacion("Días inválidos")
        return self.precio_base * dias

    def descripcion(self):
        return "Alquiler de equipos"


class Asesoria(Servicio):
    def calcular_costo(self, horas=1):
        if horas <= 0:
            raise ErrorValidacion("Horas inválidas")
        return self.precio_base * horas * 1.2

    def descripcion(self):
        return "Asesoría especializada"


# ===================== RESERVA =====================
class Reserva:
    def __init__(self, cliente, servicio):
        if not isinstance(cliente, Cliente):
            raise ErrorReserva("Cliente no válido")
        if not isinstance(servicio, Servicio):
            raise ErrorReserva("Servicio no válido")

        self.cliente = cliente
        self.servicio = servicio
        self.estado = "Pendiente"

    def confirmar(self):
        self.estado = "Confirmada"

    def cancelar(self):
        self.estado = "Cancelada"

    def mostrar(self):
        return f"{self.cliente.nombre} - {self.servicio.descripcion()} - {self.estado}"


# ===================== SISTEMA =====================
class Sistema:
    def __init__(self):
        self.clientes = []
        self.reservas = []

    def agregar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise ErrorValidacion("Cliente inválido")
        self.clientes.append(cliente)

    def crear_reserva(self, cliente, servicio):
        try:
            reserva = Reserva(cliente, servicio)
            reserva.confirmar()
            self.reservas.append(reserva)
            return reserva

        except ErrorSistema as e:
            registrar_log(f"Error controlado: {e}")
            print(f"Error: {e}")

        except Exception as e:
            registrar_log(f"Error inesperado: {e}")
            print("Ocurrió un error inesperado")

    def mostrar_reservas(self):
        if not self.reservas:
            print("No hay reservas")
            return

        for r in self.reservas:
            print(r.mostrar())


# ===================== PRUEBAS =====================
def pruebas():
    sistema = Sistema()

    try:
        # Cliente válido
        c1 = Cliente(1, "Juan")
        sistema.agregar_cliente(c1)

        # Cliente inválido
        try:
            c2 = Cliente(2, "")
        except ErrorValidacion as e:
            registrar_log(e)

        # Servicios válidos
        s1 = ReservaSala("Sala", 100)
        s2 = AlquilerEquipo("Proyector", 50)
        s3 = Asesoria("Consultoría", 200)

        # Reservas válidas
        sistema.crear_reserva(c1, s1)
        sistema.crear_reserva(c1, s2)
        sistema.crear_reserva(c1, s3)

        # Casos inválidos controlados
        sistema.crear_reserva(None, s1)  # ya NO rompe el programa
        sistema.crear_reserva(c1, None)

        sistema.mostrar_reservas()

    except Exception as e:
        registrar_log(f"Error general: {e}")


# ===================== MAIN =====================
if __name__ == "__main__":
    pruebas()
