# =============================================================================
# ARCHIVO: modulos/gestor.py
# Controlador principal. Gestiona clientes, servicios y reservas.
# =============================================================================

from modulos.cliente import Cliente
from modulos.servicios import Servicio
from modulos.reserva import Reserva
from modulos.logger import log
from modulos.excepciones import (
    ErrorClienteInvalido, ErrorServicioNoDisponible,
    ErrorReservaInvalida, ErrorDuracionInvalida,
    ErrorParametroFaltante, ErrorOperacionNoPermitida,
    ErrorCalculoCosto
)


class GestorSistema:
    """
    Controlador principal de Software FJ.
    Mantiene listas internas en memoria (sin base de datos).
    Captura todos los errores para que el sistema siga activo.
    """

    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []
        log.info("=" * 60)
        log.info("   SISTEMA SOFTWARE FJ — INICIADO")
        log.info("=" * 60)

    # ── Clientes ─────────────────────────────────────────────────────────────

    def registrar_cliente(self, nombre, email, telefono):
        """Registra cliente. Retorna None si falla."""
        try:
            if any(c.email == email.strip().lower() for c in self._clientes):
                raise ErrorClienteInvalido(
                    f"Ya existe un cliente con el email '{email}'."
                )
            cliente = Cliente(nombre, email, telefono)
            self._clientes.append(cliente)
            log.info(f"CLIENTE REGISTRADO | {cliente.describir()}")
            return cliente
        except (ErrorClienteInvalido, ErrorParametroFaltante) as ex:
            log.error(
                f"REGISTRO CLIENTE FALLIDO | "
                f"Nombre: '{nombre}' | Email: '{email}' | Error: {ex}"
            )
            return None
        except Exception as ex:
            log.critical(f"ERROR INESPERADO registrando cliente '{nombre}': {ex}")
            return None

    def buscar_cliente(self, email):
        """Retorna el cliente con ese email, o None si no existe."""
        email_buscado = email.strip().lower()
        for cliente in self._clientes:
            if cliente.email == email_buscado:
                return cliente
        return None

    def listar_clientes(self):
        return list(self._clientes)

    # ── Servicios ─────────────────────────────────────────────────────────────

    def agregar_servicio(self, servicio):
        """Agrega servicio al catálogo. Retorna True/False."""
        try:
            if servicio is None:
                raise ErrorParametroFaltante("El servicio no puede ser None.")
            if not servicio.validar():
                raise ErrorServicioNoDisponible(
                    f"El servicio '{servicio.nombre}' no pasó la validación."
                )
            self._servicios.append(servicio)
            log.info(f"SERVICIO AGREGADO | {servicio.describir()}")
            return True
        except (ErrorParametroFaltante, ErrorServicioNoDisponible) as ex:
            log.error(f"AGREGAR SERVICIO FALLIDO | Error: {ex}")
            return False

    def buscar_servicio(self, nombre):
        """Retorna el servicio con ese nombre, o None."""
        nombre_buscado = nombre.strip().lower()
        for servicio in self._servicios:
            if servicio.nombre.lower() == nombre_buscado:
                return servicio
        return None

    def listar_servicios(self):
        return list(self._servicios)

    # ── Reservas ──────────────────────────────────────────────────────────────

    def crear_reserva(self, email_cliente, nombre_servicio,
                      duracion_horas, notas=""):
        """Crea reserva en estado 'pendiente'. Retorna None si falla."""
        try:
            cliente = self.buscar_cliente(email_cliente)
            if cliente is None:
                raise ErrorReservaInvalida(
                    f"No se encontró cliente con email '{email_cliente}'."
                )
            servicio = self.buscar_servicio(nombre_servicio)
            if servicio is None:
                raise ErrorServicioNoDisponible(
                    f"No se encontró el servicio '{nombre_servicio}'."
                )
            reserva = Reserva(cliente, servicio, duracion_horas, notas)
            self._reservas.append(reserva)
            log.info(
                f"RESERVA CREADA (pendiente) | ID: {reserva.id} | "
                f"Cliente: {cliente.nombre} | "
                f"Servicio: {servicio.nombre} | "
                f"Duración: {duracion_horas}h"
            )
            return reserva
        except (ErrorReservaInvalida, ErrorServicioNoDisponible,
                ErrorDuracionInvalida, ErrorParametroFaltante,
                ErrorOperacionNoPermitida) as ex:
            log.error(f"CREAR RESERVA FALLIDA | Error: {ex}")
            return None
        except Exception as ex:
            log.critical(f"ERROR INESPERADO creando reserva: {ex}")
            return None

    def confirmar_reserva(self, reserva_id, aplicar_impuesto=True, descuento=0.0):
        """Busca y confirma reserva. Retorna -1.0 si falla."""
        try:
            reserva = next(
                (r for r in self._reservas if r.id == reserva_id), None
            )
            if reserva is None:
                raise ErrorReservaInvalida(
                    f"No se encontró reserva con ID '{reserva_id}'."
                )
            return reserva.confirmar(aplicar_impuesto, descuento)
        except (ErrorReservaInvalida, ErrorOperacionNoPermitida,
                ErrorCalculoCosto) as ex:
            log.error(f"CONFIRMAR RESERVA [{reserva_id}] FALLIDA | Error: {ex}")
            return -1.0

    def cancelar_reserva(self, reserva_id, motivo="Cancelación solicitada"):
        """Busca y cancela reserva. Retorna True/False."""
        try:
            reserva = next(
                (r for r in self._reservas if r.id == reserva_id), None
            )
            if reserva is None:
                raise ErrorReservaInvalida(
                    f"No se encontró reserva '{reserva_id}'."
                )
            reserva.cancelar(motivo)
            return True
        except (ErrorReservaInvalida, ErrorOperacionNoPermitida) as ex:
            log.error(f"CANCELAR RESERVA [{reserva_id}] FALLIDA | Error: {ex}")
            return False

    def completar_reserva(self, reserva_id):
        """Busca y completa reserva. Retorna True/False."""
        try:
            reserva = next(
                (r for r in self._reservas if r.id == reserva_id), None
            )
            if reserva is None:
                raise ErrorReservaInvalida(
                    f"No se encontró reserva '{reserva_id}'."
                )
            reserva.completar()
            return True
        except (ErrorReservaInvalida, ErrorOperacionNoPermitida) as ex:
            log.error(f"COMPLETAR RESERVA [{reserva_id}] FALLIDA | Error: {ex}")
            return False

    # ── Reporte ───────────────────────────────────────────────────────────────

    def reporte_general(self):
        """Imprime resumen del estado del sistema."""
        sep = "=" * 60
        print(f"\n{sep}")
        print("        REPORTE GENERAL — SOFTWARE FJ")
        print(sep)
        print(f"  Clientes registrados : {len(self._clientes)}")
        print(f"  Servicios en catálogo: {len(self._servicios)}")
        print(f"  Total reservas       : {len(self._reservas)}")
        print("\n  Reservas por estado:")
        for estado in Reserva.ESTADOS_VALIDOS:
            cantidad = sum(1 for r in self._reservas if r.estado == estado)
            print(f"    · {estado.capitalize():<13}: {cantidad}")
        ingresos = sum(
            r.costo_final for r in self._reservas
            if r.estado in ("confirmada", "completada")
        )
        print(f"\n  Ingresos confirmados : ${ingresos:,.2f} COP")
        print(sep)