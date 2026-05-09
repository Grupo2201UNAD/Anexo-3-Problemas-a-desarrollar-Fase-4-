# =============================================================================
# ARCHIVO: modulos/reserva.py
# Clase Reserva con try/except, try/except/else y try/except/finally
# =============================================================================

from datetime import datetime
from modulos.entidad import EntidadSistema
from modulos.logger import log
from modulos.excepciones import (
    ErrorParametroFaltante, ErrorReservaInvalida,
    ErrorServicioNoDisponible, ErrorDuracionInvalida,
    ErrorOperacionNoPermitida, ErrorCalculoCosto
)


class Reserva(EntidadSistema):
    """
    Reserva de un cliente para un servicio de Software FJ.

    Estados: pendiente → confirmada → completada
                       → cancelada
    """

    ESTADOS_VALIDOS = ("pendiente", "confirmada", "cancelada", "completada")

    def __init__(self, cliente, servicio, duracion_horas, notas=""):
        super().__init__()
        if cliente is None:
            raise ErrorParametroFaltante("Se requiere un cliente para la reserva.")
        if servicio is None:
            raise ErrorParametroFaltante("Se requiere un servicio para la reserva.")
        if not cliente.activo:
            raise ErrorReservaInvalida(f"El cliente '{cliente.nombre}' está inactivo.")
        if not servicio.disponible:
            raise ErrorServicioNoDisponible(
                f"El servicio '{servicio.nombre}' no está disponible."
            )
        servicio.validar_duracion(duracion_horas)

        self._cliente = cliente
        self._servicio = servicio
        self._duracion_horas = duracion_horas
        self._estado = "pendiente"
        self._costo_final = 0.0
        self._notas = notas.strip() if notas else ""
        self._fecha_confirmacion = None
        self._fecha_cancelacion = None

    @property
    def cliente(self): return self._cliente

    @property
    def servicio(self): return self._servicio

    @property
    def estado(self): return self._estado

    @property
    def costo_final(self): return self._costo_final

    @property
    def duracion_horas(self): return self._duracion_horas

    def confirmar(self, aplicar_impuesto=True, descuento=0.0):
        """
        Confirma la reserva usando try / except / else / finally.
        - else   : aplica cambios SOLO si no hubo error
        - finally: se ejecuta SIEMPRE
        """
        try:
            if self._estado != "pendiente":
                raise ErrorOperacionNoPermitida(
                    f"Solo se confirman reservas 'pendientes'. "
                    f"Estado actual: '{self._estado}'"
                )
            if descuento > 0.0:
                costo = self._servicio.calcular_costo_con_descuento(
                    self._duracion_horas, descuento
                )
            elif aplicar_impuesto:
                costo = self._servicio.calcular_costo_con_impuesto(
                    self._duracion_horas
                )
            else:
                costo = self._servicio.calcular_costo(self._duracion_horas)

        except (ErrorOperacionNoPermitida, ErrorCalculoCosto,
                ErrorDuracionInvalida) as ex:
            log.error(
                f"CONFIRMAR RESERVA FALLIDA | ID: {self._id} | "
                f"Cliente: {self._cliente.nombre} | Error: {ex}"
            )
            raise

        except Exception as ex:
            log.critical(f"ERROR INESPERADO confirmando reserva [{self._id}]: {ex}")
            raise ErrorCalculoCosto(
                f"Error inesperado confirmando reserva {self._id}"
            ) from ex

        else:
            # Solo se ejecuta si NO hubo excepción
            self._costo_final = costo
            self._estado = "confirmada"
            self._fecha_confirmacion = datetime.now()
            self._cliente.agregar_reserva(self)
            log.info(
                f"RESERVA CONFIRMADA | ID: {self._id} | "
                f"Cliente: {self._cliente.nombre} | "
                f"Servicio: {self._servicio.nombre} | "
                f"Duración: {self._duracion_horas}h | "
                f"Costo: ${self._costo_final:,.2f}"
            )
            return self._costo_final

        finally:
            # Se ejecuta SIEMPRE (con o sin error)
            log.debug(
                f"Intento de confirmación | "
                f"Reserva: {self._id} | Estado: {self._estado}"
            )

    def cancelar(self, motivo="Cancelado por el cliente"):
        """Cancela la reserva si está 'pendiente' o 'confirmada'."""
        try:
            if self._estado in ("cancelada", "completada"):
                raise ErrorOperacionNoPermitida(
                    f"No se puede cancelar una reserva '{self._estado}'."
                )
            self._estado = "cancelada"
            self._fecha_cancelacion = datetime.now()
            log.warning(
                f"RESERVA CANCELADA | ID: {self._id} | "
                f"Cliente: {self._cliente.nombre} | Motivo: {motivo}"
            )
        except ErrorOperacionNoPermitida as ex:
            log.error(f"CANCELACIÓN FALLIDA | ID: {self._id} | Error: {ex}")
            raise

    def completar(self):
        """Marca la reserva como completada. Solo aplica a confirmadas."""
        if self._estado != "confirmada":
            raise ErrorOperacionNoPermitida(
                f"Solo se completan reservas 'confirmadas'. "
                f"Estado actual: '{self._estado}'"
            )
        self._estado = "completada"
        log.info(
            f"RESERVA COMPLETADA | ID: {self._id} | "
            f"Cliente: {self._cliente.nombre} | "
            f"Costo cobrado: ${self._costo_final:,.2f}"
        )

    def describir(self):
        return (
            f"Reserva [{self._id}] | "
            f"Estado: {self._estado.upper()} | "
            f"Cliente: {self._cliente.nombre} | "
            f"Servicio: {self._servicio.nombre} | "
            f"Duración: {self._duracion_horas}h | "
            f"Costo: ${self._costo_final:,.2f} | "
            f"Creada: {self._fecha_creacion.strftime('%Y-%m-%d %H:%M')}"
        )

    def validar(self):
        return (
            self._cliente is not None and
            self._servicio is not None and
            self._duracion_horas > 0 and
            self._estado in self.ESTADOS_VALIDOS
        )

    def __str__(self):
        return self.describir()