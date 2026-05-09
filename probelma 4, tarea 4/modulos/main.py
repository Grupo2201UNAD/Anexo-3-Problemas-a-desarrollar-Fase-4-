from modulos.gestor import GestorSistema
from modulos.servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from modulos.excepciones import ErrorCalculoCosto, ErrorServicioNoDisponible, ErrorSistemaFJ

def separador(titulo):
    print(f"\n{'=' * 60}")
    print(f"  {titulo}")
    print(f"{'=' * 60}")

def main():
    gestor = GestorSistema()

    separador("FASE 1 - REGISTRO DE SERVICIOS")

    print("\n[OP-01] Sala Conferencias A (VALIDO)...")
    try:
        sala_a = ReservaSala("Sala Conferencias A", 80000, capacidad=20)
        gestor.agregar_servicio(sala_a)
        print(f"  OK {sala_a.describir()}")
    except ErrorSistemaFJ as ex:
        print(f"  ERROR {ex}")

    print("\n[OP-02] Sala con precio negativo (DEBE FALLAR)...")
    try:
        ReservaSala("Sala Invalida", -5000, capacidad=10)
    except ErrorServicioNoDisponible as ex:
        print(f"  ERROR Capturado: {ex}")

    print("\n[OP-03] Laptop HP EliteBook (VALIDO)...")
    try:
        laptop = AlquilerEquipo("Laptop HP EliteBook", 25000, "Laptop")
        gestor.agregar_servicio(laptop)
        print(f"  OK {laptop.describir()}")
    except ErrorSistemaFJ as ex:
        print(f"  ERROR {ex}")

    print("\n[OP-04] Asesoria Arquitectura Software (VALIDO)...")
    try:
        asesoria = AsesoriaEspecializada(
            "Asesoria Arquitectura Software", 120000,
            area="Ingenieria de Software",
            nivel_asesor="senior", cargo_sesion=50000)
        gestor.agregar_servicio(asesoria)
        print(f"  OK {asesoria.describir()}")
    except ErrorSistemaFJ as ex:
        print(f"  ERROR {ex}")

    print("\n[OP-05] Asesoria nivel=maestro (DEBE FALLAR)...")
    try:
        AsesoriaEspecializada("X", 100000, "Test", nivel_asesor="maestro")
    except ErrorServicioNoDisponible as ex:
        print(f"  ERROR Capturado: {ex}")

    separador("FASE 2 - REGISTRO DE CLIENTES")

    print("\n[OP-06] Ana Garcia Lopez (VALIDO)...")
    ana = gestor.registrar_cliente(
        "Ana Garcia Lopez", "ana.garcia@empresa.com", "3001234567")
    if ana:
        print(f"  OK {ana.describir()}")

    print("\n[OP-07] Carlos Mendoza Ruiz (VALIDO)...")
    carlos = gestor.registrar_cliente(
        "Carlos Mendoza Ruiz", "carlos.m@startup.co", "+57 310 987 6543")
    if carlos:
        print(f"  OK {carlos.describir()}")

    print("\n[OP-08] Email invalido (DEBE FALLAR)...")
    r = gestor.registrar_cliente("Pedro Sin Email", "no-es-email", "3009999999")
    if r is None:
        print("  ERROR Rechazado correctamente (email invalido).")

    print("\n[OP-09] Email duplicado (DEBE FALLAR)...")
    r = gestor.registrar_cliente("Ana Copia", "ana.garcia@empresa.com", "3001111111")
    if r is None:
        print("  ERROR Rechazado correctamente (email duplicado).")

    print("\n[OP-10] Nombre de 2 letras (DEBE FALLAR)...")
    r = gestor.registrar_cliente("AB", "ab@test.com", "3001111111")
    if r is None:
        print("  ERROR Rechazado correctamente (nombre muy corto).")

    separador("FASE 3 - GESTION DE RESERVAS")

    print("\n[OP-11] Ana reserva Sala por 3 horas (VALIDO)...")
    reserva_sala = gestor.crear_reserva(
        "ana.garcia@empresa.com", "Sala Conferencias A", 3, "Kick-off Alfa")
    if reserva_sala:
        print(f"  OK {reserva_sala.describir()}")

    print("\n[OP-12] Confirmar sala con IVA (VALIDO)...")
    if reserva_sala:
        costo = gestor.confirmar_reserva(reserva_sala.id, aplicar_impuesto=True)
        if costo > 0:
            print(f"  OK Confirmada. Costo con IVA: ${costo:,.2f} COP")

    print("\n[OP-13] Carlos reserva Laptop por 5 horas (VALIDO)...")
    reserva_laptop = gestor.crear_reserva(
        "carlos.m@startup.co", "Laptop HP EliteBook", 5)
    if reserva_laptop:
        print(f"  OK {reserva_laptop.describir()}")

    print("\n[OP-14] Confirmar laptop con 15% descuento (VALIDO)...")
    if reserva_laptop:
        costo = gestor.confirmar_reserva(
            reserva_laptop.id, aplicar_impuesto=False, descuento=0.15)
        if costo > 0:
            print(f"  OK Confirmada con descuento. Costo: ${costo:,.2f} COP")

    print("\n[OP-15] Ana reserva Asesoria por 2 horas (VALIDO)...")
    reserva_asesoria = gestor.crear_reserva(
        "ana.garcia@empresa.com", "Asesoria Arquitectura Software", 2, "Revision MVC")
    if reserva_asesoria:
        costo = gestor.confirmar_reserva(reserva_asesoria.id)
        if costo > 0:
            print(f"  OK Confirmada. Costo asesoria: ${costo:,.2f} COP")

    print("\n[OP-16] Confirmar sala ya confirmada (DEBE FALLAR)...")
    if reserva_sala:
        r = gestor.confirmar_reserva(reserva_sala.id)
        if r < 0:
            print("  ERROR Capturado correctamente (ya confirmada).")

    print("\n[OP-17] Asesoria por 10h max=6h (DEBE FALLAR)...")
    r = gestor.crear_reserva(
        "ana.garcia@empresa.com", "Asesoria Arquitectura Software", 10)
    if r is None:
        print("  ERROR Rechazada correctamente (duracion fuera de rango).")

    print("\n[OP-18] Carlos cancela laptop (VALIDO)...")
    if reserva_laptop:
        ok = gestor.cancelar_reserva(reserva_laptop.id, "Cambio de planes")
        if ok:
            print(f"  OK Cancelada. Estado: {reserva_laptop.estado}")

    print("\n[OP-19] Cancelar laptop ya cancelada (DEBE FALLAR)...")
    if reserva_laptop:
        ok = gestor.cancelar_reserva(reserva_laptop.id)
        if not ok:
            print("  ERROR Capturado correctamente (ya cancelada).")

    print("\n[OP-20] Reserva con cliente inexistente (DEBE FALLAR)...")
    r = gestor.crear_reserva("noexiste@correo.com", "Sala Conferencias A", 2)
    if r is None:
        print("  ERROR Rechazada correctamente (cliente no registrado).")

    print("\n[OP-21] Reserva de sala deshabilitada (DEBE FALLAR)...")
    sala_a.deshabilitar()
    r = gestor.crear_reserva("ana.garcia@empresa.com", "Sala Conferencias A", 1)
    if r is None:
        print("  ERROR Rechazada correctamente (servicio no disponible).")
    sala_a.habilitar()

    print("\n[OP-22] Completar asesoria de Ana (VALIDO)...")
    if reserva_asesoria and reserva_asesoria.estado == "confirmada":
        ok = gestor.completar_reserva(reserva_asesoria.id)
        if ok:
            print(f"  OK Completada. Estado: {reserva_asesoria.estado}")

    print("\n[OP-23] Paquete 3 sesiones x 2h con 15% dto (VALIDO)...")
    try:
        costo = asesoria.calcular_costo_paquete(sesiones=3, horas_por_sesion=2)
        print(f"  OK Costo paquete: ${costo:,.2f} COP")
    except ErrorCalculoCosto as ex:
        print(f"  ERROR {ex}")

    print("\n[OP-24] Descuento 50% en asesoria max=30% (DEBE FALLAR)...")
    try:
        asesoria.calcular_costo_con_descuento(2, 0.50)
    except ErrorCalculoCosto as ex:
        print(f"  ERROR Capturado: {ex}")

    gestor.reporte_general()

    print("\n" + "=" * 60)
    print("  SIMULACION COMPLETADA")
    print("  Revise el archivo: logs/software_fj.log")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()