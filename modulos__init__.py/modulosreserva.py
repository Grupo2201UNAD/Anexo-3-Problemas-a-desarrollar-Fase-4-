@"
from datetime import datetime
from modulos.entidad import EntidadSistema
from modulos.logger import log
from modulos.excepciones import (
    ErrorParametroFaltante, ErrorReservaInvalida,
    ErrorServicioNoDisponible, ErrorDuracionInvalida,
    ErrorOperacionNoPermitida, ErrorCalculoCosto
)

class Reserva(EntidadSistema):
    ESTADOS_VALIDOS = ("pendiente", "confirmada", "cancelada", "completada")
    def __init__(self, cliente, servicio, duracion_horas, notas=""):
        super().__init__()
        if cliente is None:
            raise ErrorParametroFaltante("Se requiere un cliente para la reserva.")
        if servicio is None:
            raise ErrorParametroFaltante("Se requiere un servicio para la reserva.")
        if not cliente.activo:
            raise ErrorReservaInvalida(f"El cliente '{cliente.nombre}' esta inactivo.")
        if not servicio.disponible:
            raise ErrorServicioNoDisponible(f"El servicio '{servicio.nombre}' no esta disponible.")
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
        try:
            if self._estado != "pendiente":
                raise ErrorOperacionNoPermitida(
                    f"Solo se confirman reservas 'pendientes'. Estado actual: '{self._estado}'")
            if descuento > 0.0:
                costo = self._servicio.calcular_costo_con_descuento(self._duracion_horas, descuento)
            elif aplicar_impuesto:
                costo = self._servicio.calcular_costo_con_impuesto(self._duracion_horas)
            else:
                costo = self._servicio.calcular_costo(self._duracion_horas)
        except (ErrorOperacionNoPermitida, ErrorCalculoCosto, ErrorDuracionInvalida) as ex:
            log.error(f"CONFIRMAR RESERVA FALLIDA | ID: {self._id} | Cliente: {self._cliente.nombre} | Error: {ex}")
            raise
        except Exception as ex:
            log.critical(f"ERROR INESPERADO confirmando [{self._id}]: {ex}")
            raise ErrorCalculoCosto(f"Error inesperado confirmando reserva {self._id}") from ex
        else:
            self._costo_final = costo
            self._estado = "confirmada"
            self._fecha_confirmacion = datetime.now()
            self._cliente.agregar_reserva(self)
            log.info(f"RESERVA CONFIRMADA | ID: {self._id} | Cliente: {self._cliente.nombre} | "
                     f"Servicio: {self._servicio.nombre} | Duracion: {self._duracion_horas}h | Costo: \${self._costo_final:,.2f}")
            return self._costo_final
        finally:
            log.debug(f"Intento de confirmacion | Reserva: {self._id} | Estado: {self._estado}")
    def cancelar(self, motivo="Cancelado por el cliente"):
        try:
            if self._estado in ("cancelada", "completada"):
                raise ErrorOperacionNoPermitida(f"No se puede cancelar una reserva '{self._estado}'.")
            self._estado = "cancelada"
            self._fecha_cancelacion = datetime.now()
            log.warning(f"RESERVA CANCELADA | ID: {self._id} | Cliente: {self._cliente.nombre} | Motivo: {motivo}")
        except ErrorOperacionNoPermitida as ex:
            log.error(f"CANCELACION FALLIDA | ID: {self._id} | Error: {ex}")
            raise
    def completar(self):
        if self._estado != "confirmada":
            raise ErrorOperacionNoPermitida(
                f"Solo se completan reservas 'confirmadas'. Estado actual: '{self._estado}'")
        self._estado = "completada"
        log.info(f"RESERVA COMPLETADA | ID: {self._id} | Cliente: {self._cliente.nombre} | Costo: \${self._costo_final:,.2f}")
    def describir(self):
        return (f"Reserva [{self._id}] | Estado: {self._estado.upper()} | "
                f"Cliente: {self._cliente.nombre} | Servicio: {self._servicio.nombre} | "
                f"Duracion: {self._duracion_horas}h | Costo: \${self._costo_final:,.2f} | "
                f"Creada: {self._fecha_creacion.strftime('%Y-%m-%d %H:%M')}")
    def validar(self):
        return (self._cliente is not None and self._servicio is not None
                and self._duracion_horas > 0 and self._estado in self.ESTADOS_VALIDOS)
    def __str__(self): return self.describir()
"@ | Out-File -FilePath "modulos\reserva.py" -Encoding utf8