@'
from abc import abstractmethod
from modulos.entidad import EntidadSistema
from modulos.excepciones import (
    ErrorServicioNoDisponible, ErrorDuracionInvalida,
    ErrorParametroFaltante, ErrorCalculoCosto
)

class Servicio(EntidadSistema):
    IMPUESTO_DEFAULT = 0.19
    def __init__(self, nombre, precio_base, duracion_min=1, duracion_max=8):
        super().__init__()
        if not nombre or not nombre.strip():
            raise ErrorParametroFaltante("El nombre del servicio es obligatorio.")
        if precio_base <= 0:
            raise ErrorServicioNoDisponible(f"El precio debe ser mayor a 0. Recibido: {precio_base}")
        if duracion_min < 1 or duracion_max < duracion_min:
            raise ErrorDuracionInvalida(f"Rango invalido: min={duracion_min}h, max={duracion_max}h")
        self._nombre = nombre.strip()
        self._precio_base = float(precio_base)
        self._disponible = True
        self._duracion_min = duracion_min
        self._duracion_max = duracion_max
    @property
    def nombre(self): return self._nombre
    @property
    def precio_base(self): return self._precio_base
    @property
    def disponible(self): return self._disponible
    def deshabilitar(self): self._disponible = False
    def habilitar(self): self._disponible = True
    def validar_duracion(self, duracion_horas):
        if not isinstance(duracion_horas, int) or duracion_horas < 1:
            raise ErrorDuracionInvalida(f"La duracion debe ser entero positivo. Recibido: '{duracion_horas}'")
        if duracion_horas < self._duracion_min or duracion_horas > self._duracion_max:
            raise ErrorDuracionInvalida(
                f"Duracion {duracion_horas}h fuera del rango [{self._duracion_min}h-{self._duracion_max}h] para '{self._nombre}'")
        return True
    def validar(self): return self._disponible and self._precio_base > 0
    @abstractmethod
    def calcular_costo(self, duracion_horas): pass
    @abstractmethod
    def calcular_costo_con_impuesto(self, duracion_horas, tasa_impuesto=None): pass
    @abstractmethod
    def calcular_costo_con_descuento(self, duracion_horas, porcentaje_descuento): pass
    def __str__(self): return self.describir()

class ReservaSala(Servicio):
    _RECARGO_POR_PERSONA = 5000
    def __init__(self, nombre, precio_base, capacidad):
        super().__init__(nombre, precio_base, duracion_min=1, duracion_max=12)
        if capacidad < 1:
            raise ErrorServicioNoDisponible("La capacidad minima es 1 persona.")
        self._capacidad = capacidad
    @property
    def capacidad(self): return self._capacidad
    def calcular_costo(self, duracion_horas):
        try:
            self.validar_duracion(duracion_horas)
            return round(self._precio_base * duracion_horas, 2)
        except ErrorDuracionInvalida: raise
        except Exception as ex:
            raise ErrorCalculoCosto(f"Error en costo de sala '{self._nombre}'") from ex
    def calcular_costo_con_impuesto(self, duracion_horas, tasa_impuesto=None):
        tasa = tasa_impuesto if tasa_impuesto is not None else self.IMPUESTO_DEFAULT
        return round(self.calcular_costo(duracion_horas) * (1 + tasa), 2)
    def calcular_costo_con_descuento(self, duracion_horas, porcentaje_descuento):
        if not (0.0 <= porcentaje_descuento <= 1.0):
            raise ErrorCalculoCosto(f"Descuento {porcentaje_descuento} invalido.")
        return round(self.calcular_costo(duracion_horas) * (1 - porcentaje_descuento), 2)
    def calcular_costo_con_personas(self, duracion_horas, num_personas):
        costo = self.calcular_costo(duracion_horas)
        mitad = self._capacidad // 2
        if num_personas > mitad:
            return round(costo + (num_personas - mitad) * self._RECARGO_POR_PERSONA, 2)
        return costo
    def describir(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return (f"[SALA] {self._nombre} | Capacidad: {self._capacidad} personas | "
                f"Precio: ${self._precio_base:,.0f}/h | "
                f"Rango: {self._duracion_min}h-{self._duracion_max}h | {estado}")

class AlquilerEquipo(Servicio):
    _PORCENTAJE_DEPOSITO = 0.20
    def __init__(self, nombre, precio_base, tipo_equipo):
        super().__init__(nombre, precio_base, duracion_min=1, duracion_max=24)
        if not tipo_equipo or not tipo_equipo.strip():
            raise ErrorParametroFaltante("El tipo de equipo es obligatorio.")
        self._tipo_equipo = tipo_equipo.strip()
    @property
    def tipo_equipo(self): return self._tipo_equipo
    def calcular_costo(self, duracion_horas):
        try:
            self.validar_duracion(duracion_horas)
            if duracion_horas > 8:
                return round(self._precio_base * duracion_horas * 0.90, 2)
            return round(self._precio_base * duracion_horas, 2)
        except ErrorDuracionInvalida: raise
        except Exception as ex:
            raise ErrorCalculoCosto(f"Error en costo de equipo '{self._nombre}'") from ex
    def calcular_costo_con_impuesto(self, duracion_horas, tasa_impuesto=None):
        tasa = tasa_impuesto if tasa_impuesto is not None else self.IMPUESTO_DEFAULT
        costo = self.calcular_costo(duracion_horas)
        return round(costo * (1 + tasa) + costo * self._PORCENTAJE_DEPOSITO, 2)
    def calcular_costo_con_descuento(self, duracion_horas, porcentaje_descuento):
        if porcentaje_descuento > 0.50:
            raise ErrorCalculoCosto("El descuento maximo para equipos es del 50%.")
        return round(self.calcular_costo(duracion_horas) * (1 - porcentaje_descuento), 2)
    def calcular_deposito(self, duracion_horas):
        return round(self.calcular_costo(duracion_horas) * self._PORCENTAJE_DEPOSITO, 2)
    def describir(self):
        estado = "Disponible" if self._disponible else "No disponible"
        return (f"[EQUIPO] {self._nombre} ({self._tipo_equipo}) | "
                f"Precio: ${self._precio_base:,.0f}/h | "
                f"Rango: {self._duracion_min}h-{self._duracion_max}h | Deposito: 20% | {estado}")

class AsesoriaEspecializada(Servicio):
    _MULTIPLICADORES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}
    def __init__(self, nombre, precio_base, area, nivel_asesor="junior", cargo_sesion=0):
        super().__init__(nombre, precio_base, duracion_min=1, duracion_max=6)
        if not area or not area.strip():
            raise ErrorParametroFaltante("El area de asesoria es obligatoria.")
        nivel = nivel_asesor.lower().strip()
        if nivel not in self._MULTIPLICADORES:
            raise ErrorServicioNoDisponible(
                f"Nivel '{nivel_asesor}' no valido. Use: {list(self._MULTIPLICADORES.keys())}")
        self._area = area.strip()
        self._nivel_asesor = nivel
        self._cargo_sesion = float(cargo_sesion) if cargo_sesion >= 0 else 0.0
    @property
    def area(self): return self._area
    @property
    def nivel_asesor(self): return self._nivel_asesor
    def calcular_costo(self, duracion_horas):
        try:
            self.validar_duracion(duracion_horas)
            mult = self._MULTIPLICADORES[self._nivel_asesor]
            return round(self._precio_base * mult * duracion_horas + self._cargo_sesion, 2)
        except ErrorDuracionInvalida: raise
        except Exception as ex:
            raise ErrorCalculoCosto(f"Error en costo de asesoria '{self._nombre}'") from ex
    def calcular_costo_con_impuesto(self, duracion_horas, tasa_impuesto=None):
        tasa = tasa_impuesto if tasa_impuesto is not None else self.IMPUESTO_DEFAULT
        return round(self.calcular_costo(duracion_horas) * (1 + tasa), 2)
    def calcular_costo_con_descuento(self, duracion_horas, porcentaje_descuento):
        if not (0.0 <= porcentaje_descuento <= 0.30):
            raise ErrorCalculoCosto("El descuento maximo en asesorias es del 30%.")
        mult = self._MULTIPLICADORES[self._nivel_asesor]
        costo_horas = self._precio_base * mult * duracion_horas
        return round(costo_horas * (1 - porcentaje_descuento) + self._cargo_sesion, 2)
    def calcular_costo_paquete(self, sesiones, horas_por_sesion):
        if sesiones < 2:
            raise ErrorCalculoCosto("Los paquetes requieren minimo 2 sesiones.")
        return round(self.calcular_costo(horas_por_sesion) * sesiones * 0.85, 2)
    def describir(self):
        estado = "Disponible" if self._disponible else "No disponible"
        mult = self._MULTIPLICADORES[self._nivel_asesor]
        return (f"[ASESORIA] {self._nombre} | Area: {self._area} | "
                f"Nivel: {self._nivel_asesor.capitalize()} (x{mult}) | "
                f"Precio: ${self._precio_base:,.0f}/h | "
                f"Cargo sesion: ${self._cargo_sesion:,.0f} | {estado}")
'@ | Out-File -FilePath "modulos\servicios.py" -Encoding utf8