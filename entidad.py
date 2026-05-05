# =============================================================================
# ARCHIVO 3: modulos/entidad.py
# DESCRIPCIÓN: Clase abstracta base. Toda entidad del sistema hereda de aquí.
# PRINCIPIO OOP: Abstracción
# =============================================================================

import uuid                            # Para generar IDs únicos
from abc import ABC, abstractmethod    # ABC = Abstract Base Class
from datetime import datetime          # Para la fecha de creación


class EntidadSistema(ABC):
    """
    Clase abstracta base del sistema Software FJ.

    NO se puede instanciar directamente (es abstracta).
    Solo sirve como plantilla para Cliente, Servicio y Reserva.

    Toda subclase DEBE implementar:
        - describir() → str
        - validar()   → bool

    Genera automáticamente:
        _id (str)              : ID único de 8 caracteres en mayúsculas
        _fecha_creacion        : Fecha y hora exacta de creación
    """

    def __init__(self):
        """
        Constructor base. Se llama con super().__init__() desde las subclases.
        Genera el ID único y registra la fecha de creación.
        """
        # uuid.uuid4() genera un ID aleatorio
        # [:8] toma solo los primeros 8 caracteres
        # .upper() los pone en mayúsculas → ejemplo: 'A3F8C1D2'
        self._id = str(uuid.uuid4())[:8].upper()

        # Captura el momento exacto de creación del objeto
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        """Retorna el ID único. Solo lectura (sin setter)."""
        return self._id

    @property
    def fecha_creacion(self):
        """Retorna la fecha de creación. Solo lectura."""
        return self._fecha_creacion

    @abstractmethod
    def describir(self):
        """
        Cada subclase DEBE implementar este método.
        Retorna una descripción textual del objeto.
        """
        pass   # Sin código aquí; lo pone la subclase

    @abstractmethod
    def validar(self):
        """
        Cada subclase DEBE implementar este método.
        Retorna True si el objeto es válido, False si no.
        """
        pass

    def __repr__(self):
        """
        Representación técnica del objeto para depuración.
        Ejemplo: Cliente(id=A3F8C1D2)
        """
        return f"{self.__class__.__name__}(id={self._id})"