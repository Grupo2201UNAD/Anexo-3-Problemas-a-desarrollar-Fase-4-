# =============================================================================
# ARCHIVO 1: modulos/excepciones.py
# DESCRIPCIÓN: Todas las excepciones personalizadas del sistema.
# =============================================================================


class ErrorSistemaFJ(Exception):
    """
    Excepción BASE del sistema Software FJ.
    Todas las demás heredan de esta.
    Permite capturarlas todas con: except ErrorSistemaFJ
    """
    pass


class ErrorClienteInvalido(ErrorSistemaFJ):
    """
    Se lanza cuando los datos de un cliente son inválidos.
    Ejemplo: email mal escrito, nombre muy corto.
    """
    pass


class ErrorServicioNoDisponible(ErrorSistemaFJ):
    """
    Se lanza cuando el servicio no está disponible
    o sus parámetros de creación son incorrectos.
    Ejemplo: precio negativo, nivel de asesor inválido.
    """
    pass


class ErrorReservaInvalida(ErrorSistemaFJ):
    """
    Se lanza cuando los parámetros de una reserva son incorrectos.
    Ejemplo: cliente inactivo, servicio no encontrado.
    """
    pass


class ErrorDuracionInvalida(ErrorSistemaFJ):
    """
    Se lanza cuando la duración está fuera del rango permitido.
    Ejemplo: 0 horas, más horas que el máximo del servicio.
    """
    pass


class ErrorParametroFaltante(ErrorSistemaFJ):
    """
    Se lanza cuando falta un campo obligatorio.
    Ejemplo: nombre vacío, servicio None.
    """
    pass


class ErrorOperacionNoPermitida(ErrorSistemaFJ):
    """
    Se lanza cuando la operación no es válida en el estado actual.
    Ejemplo: confirmar una reserva ya confirmada.
    """
    pass


class ErrorCalculoCosto(ErrorSistemaFJ):
    """
    Se lanza cuando falla el cálculo del costo de un servicio.
    Ejemplo: descuento fuera de rango.
    """
    pass