# =============================================================================
# ARCHIVO 4: modulos/cliente.py
# DESCRIPCIÓN: Clase Cliente con encapsulación y validaciones robustas.
# PRINCIPIOS OOP: Herencia (de EntidadSistema), Encapsulación
# =============================================================================

import re   # Expresiones regulares para validar email y teléfono

from modulos.entidad import EntidadSistema
from modulos.excepciones import ErrorClienteInvalido, ErrorParametroFaltante


class Cliente(EntidadSistema):
    """
    Representa un cliente registrado en Software FJ.

    Encapsulación total: todos los atributos son privados (_nombre, etc.)
    y solo se acceden mediante @property y setters con validación.

    Validaciones:
        - Nombre  : mínimo 3 caracteres, no vacío
        - Email   : formato válido (usuario@dominio.com)
        - Teléfono: solo dígitos, entre 7 y 15 caracteres
    """

    # Patrón para validar email: usuario@dominio.extension
    _PATRON_EMAIL = re.compile(r"^[\w.\-+]+@[\w.\-]+\.[a-zA-Z]{2,}$")

    # Patrón para teléfono: + opcional, dígitos, espacios, guiones (7-15 chars)
    _PATRON_TELEFONO = re.compile(r"^\+?[\d\s\-]{7,15}$")

    def __init__(self, nombre, email, telefono):
        """
        Inicializa el cliente. Llama a super() para obtener ID y fecha.
        Asigna campos usando setters (activan las validaciones).

        Raises:
            ErrorParametroFaltante: Campo vacío u omitido
            ErrorClienteInvalido  : Dato que no pasa la validación
        """
        super().__init__()       # Genera self._id y self._fecha_creacion

        self.nombre = nombre     # → activa @nombre.setter (valida)
        self.email = email       # → activa @email.setter  (valida)
        self.telefono = telefono # → activa @telefono.setter (valida)

        self._activo = True      # Todo cliente inicia activo
        self._reservas = []      # Lista vacía de reservas

    # ── Getter y Setter: nombre ──────────────────────────────────────────────

    @property
    def nombre(self):
        """Retorna el nombre del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        """Valida y asigna el nombre."""
        if not valor or not valor.strip():
            # Campo vacío o solo espacios en blanco
            raise ErrorParametroFaltante("El nombre no puede estar vacío.")
        if len(valor.strip()) < 3:
            # Nombre demasiado corto (ej: "AB")
            raise ErrorClienteInvalido("El nombre debe tener al menos 3 caracteres.")
        self._nombre = valor.strip()   # Guarda sin espacios extremos

    # ── Getter y Setter: email ───────────────────────────────────────────────

    @property
    def email(self):
        """Retorna el email del cliente."""
        return self._email

    @email.setter
    def email(self, valor):
        """Valida el formato del email con regex."""
        if not valor or not valor.strip():
            raise ErrorParametroFaltante("El email no puede estar vacío.")
        if not self._PATRON_EMAIL.match(valor.strip()):
            raise ErrorClienteInvalido(
                f"El email '{valor}' no es válido. Use: usuario@dominio.com"
            )
        self._email = valor.strip().lower()  # Guarda en minúsculas

    # ── Getter y Setter: teléfono ────────────────────────────────────────────

    @property
    def telefono(self):
        """Retorna el teléfono del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        """Valida el formato del teléfono con regex."""
        if not valor or not valor.strip():
            raise ErrorParametroFaltante("El teléfono no puede estar vacío.")
        if not self._PATRON_TELEFONO.match(valor.strip()):
            raise ErrorClienteInvalido(
                f"El teléfono '{valor}' no es válido. Use 7-15 dígitos."
            )
        self._telefono = valor.strip()

    # ── Propiedades de solo lectura ──────────────────────────────────────────

    @property
    def activo(self):
        """True si el cliente está activo, False si fue desactivado."""
        return self._activo

    @property
    def reservas(self):
        """
        Retorna COPIA de la lista de reservas.
        Se retorna copia para que nadie modifique la lista interna
        directamente desde afuera → encapsulación.
        """
        return list(self._reservas)

    # ── Métodos ──────────────────────────────────────────────────────────────

    def agregar_reserva(self, reserva):
        """Agrega una reserva confirmada al historial del cliente."""
        self._reservas.append(reserva)

    def desactivar(self):
        """Marca al cliente como inactivo (no puede hacer nuevas reservas)."""
        self._activo = False

    def describir(self):
        """Implementa el método abstracto de EntidadSistema."""
        estado = "Activo" if self._activo else "Inactivo"
        return (
            f"Cliente [{self._id}] | "
            f"Nombre: {self._nombre} | "
            f"Email: {self._email} | "
            f"Tel: {self._telefono} | "
            f"Estado: {estado} | "
            f"Reservas: {len(self._reservas)}"
        )

    def validar(self):
        """Verifica que todos los campos están asignados correctamente."""
        return bool(self._nombre and self._email and self._telefono)

    def __str__(self):
        return self.describir()


# ── PRUEBA DIRECTA (solo se ejecuta con: python modulos/cliente.py) ──────────
if __name__ == "__main__":
    print("=== PRUEBA CLASE CLIENTE ===\n")

    # Prueba 1: Cliente válido
    try:
        c1 = Cliente("Ana García López", "ana@empresa.com", "3001234567")
        print(f"✔ Cliente creado: {c1}")
    except Exception as e:
        print(f"✘ Error inesperado: {e}")

    # Prueba 2: Email inválido
    try:
        c2 = Cliente("Pedro López", "no-es-email", "3001111111")
    except ErrorClienteInvalido as e:
        print(f"✔ Error capturado (email inválido): {e}")

    # Prueba 3: Nombre muy corto
    try:
        c3 = Cliente("AB", "ab@test.com", "3009999999")
    except ErrorClienteInvalido as e:
        print(f"✔ Error capturado (nombre corto): {e}")

    # Prueba 4: Teléfono vacío
    try:
        c4 = Cliente("María Ruiz", "maria@test.com", "")
    except ErrorParametroFaltante as e:
        print(f"✔ Error capturado (teléfono vacío): {e}")