# =============================================================================
# ARCHIVO 2: modulos/logger.py
# DESCRIPCIÓN: Configura el sistema de registro de eventos (logs).
#              Guarda todo en archivo y muestra mensajes en consola.
# =============================================================================

import logging   # Módulo estándar de Python para logs
import os        # Para crear carpetas si no existen


def configurar_logger(nombre="SoftwareFJ",
                      ruta_log="logs/software_fj.log"):
    """
    Crea y configura el logger principal.

    Args:
        nombre   : Nombre del logger (aparece en cada línea del log)
        ruta_log : Ruta del archivo donde se guardan los registros

    Returns:
        logging.Logger: Logger listo para usar
    """

    # Crea la carpeta 'logs/' automáticamente si no existe
    os.makedirs(os.path.dirname(ruta_log), exist_ok=True)

    # Obtener el logger con el nombre indicado
    logger = logging.getLogger(nombre)

    # DEBUG captura todos los niveles: debug, info, warning, error, critical
    logger.setLevel(logging.DEBUG)

    # Formato de cada línea del log:
    # Ejemplo: 2025-05-01 10:23:45 | INFO     | Mensaje aquí
    formato = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler 1: Guarda TODO en el archivo (nivel DEBUG)
    manejador_archivo = logging.FileHandler(ruta_log, encoding="utf-8", mode="a")
    manejador_archivo.setLevel(logging.DEBUG)      # Guarda todo
    manejador_archivo.setFormatter(formato)         # Aplica el formato

    # Handler 2: Muestra en consola solo INFO en adelante (no DEBUG)
    manejador_consola = logging.StreamHandler()
    manejador_consola.setLevel(logging.INFO)       # Info, warning, error
    manejador_consola.setFormatter(formato)

    # Agregar handlers SOLO si el logger no los tiene ya
    # (evita duplicar mensajes si se llama varias veces)
    if not logger.handlers:
        logger.addHandler(manejador_archivo)
        logger.addHandler(manejador_consola)

    return logger   # Retorna el logger configurado


# Instancia global: se importa en los demás archivos con:
# from modulos.logger import log
log = configurar_logger()