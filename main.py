"""
Módulo: main.py
Responsable: Juan Camilo Bohorquez
Descripción: Punto de entrada que simula 12 operaciones válidas e inválidas en Software FJ.
Version: 1.0
"""

from excepciones import ReservaInvalidaError, SoftwareFJError  # Excepciones personalizadas
from gestores import GestorClientes, GestorReservas, GestorServicios  # Capa de negocio
from logger_config import configurar_logger  # Configuración de logs en archivo y consola
from repositorios import ClienteRepositorio, ReservaRepositorio, ServicioRepositorio  #Repositorio de datos persistente de memoria


def main():
    """Ejecuta la batería de simulación integral del sistema Software FJ."""
    logger = configurar_logger()  # Aqui se inicializa el gestor de logs
    print("=== INICIO DE SIMULACIÓN INTEGRAL - SOFTWARE FJ ===\n")
    logger.info("-INICIO DE SESIÓN DE SIMULACIÓN-")

    # 1. Inicialización de repositorios en memoria 
    repo_clientes = ClienteRepositorio()
    repo_servicios = ServicioRepositorio()
    repo_reservas = ReservaRepositorio()

    # 2. Inicialización de gestores de negocio
    gestor_clientes = GestorClientes(repo_clientes)
    gestor_servicios = GestorServicios(repo_servicios)
    gestor_reservas = GestorReservas(repo_reservas, repo_clientes, repo_servicios)
    # Aqui se incian las simulaciones de las operaciones del sistema se software
    # [Operación 1] Registro válido de cliente
    try:
        print("[Op 1] Registrando cliente válido...")
        c1 = gestor_clientes.registrar_cliente(
            "1020304050", "Ana María Gómez", "ana.gomez@mail.com", "3104567890"
        )
        print(f" -> Éxito: {c1.obtener_detalles()}")
    except SoftwareFJError as e:
        print(f" -> Error capturado: {e}")

    # [Operación 2] Registro inválido de cliente (cédula alfanumérica)
    try:
        print("\n[Op 2] Intentando registrar cliente con cédula inválida...")
        gestor_clientes.registrar_cliente("1020ABC", "Carlos Pérez", "carlos@mail.com", "3201234567")
    except SoftwareFJError as e:
        print(f" -> Error controlado correctamente: {e}")
        logger.warning(f"Op 2 controlada: {e}")

    # [Operación 3] Registro inválido de cliente (correo sin formato válido)
    try:
        print("\n[Op 3] Intentando registrar cliente con correo inválido...")
        gestor_clientes.registrar_cliente("987654321", "Laura Torres", "laura_sin_arroba.com", "3009876543")
    except SoftwareFJError as e:
        print(f" -> Error controlado correctamente: {e}")
        logger.warning(f"Op 3 controlada: {e}")

    # [Operación 4] Creación válida de servicio tipo Sala
    try:
        print("\n[Op 4] Creando servicio de reserva de sala...")
        s1 = gestor_servicios.crear_servicio(
            "sala", id_servicio="SR-01", nombre="Sala de Juntas Ejecutiva", tarifa_base=50.0, capacidad=15
        )
        print(f" -> Éxito: {s1.obtener_detalles()}")
    except SoftwareFJError as e:
        print(f" -> Error: {e}")

    # [Operación 5] Creación inválida de servicio (tarifa negativa)
    try:
        print("\n[Op 5] Intentando crear servicio con tarifa negativa...")
        gestor_servicios.crear_servicio(
            "equipo", id_servicio="EQ-01", nombre="Proyector 4K", tarifa_base=-150.0, tipo_equipo="Audiovisual"
        )
    except SoftwareFJError as e:
        print(f" -> Error controlado correctamente: {e}")
        logger.warning(f"Op 5 controlada: {e}")

    # [Operación 6] Creación inválida de servicio (parámetro faltante)
    try:
        print("\n[Op 6] Intentando crear servicio con parámetros faltantes...")
        gestor_servicios.crear_servicio("asesoria", id_servicio="AS-ERR", nombre="Auditoría", tarifa_base=70.0)
    except SoftwareFJError as e:
        print(f" -> Error controlado correctamente: {e}")
        logger.warning(f"Op 6 controlada: {e}")

    # [Operación 7] Creación válida de servicios de Equipo y Asesoría
    try:
        print("\n[Op 7] Creando servicios de equipos y asesoría especializada...")
        s2 = gestor_servicios.crear_servicio(
            "equipo", id_servicio="EQ-02", nombre="Laptop Core i7", tarifa_base=25.0, tipo_equipo="Cómputo"
        )
        s3 = gestor_servicios.crear_servicio(
            "asesoria", id_servicio="AS-01", nombre="Arquitectura Cloud", tarifa_base=80.0, area_experto="Tecnología"
        )
        print(f" -> Éxito: {s2.obtener_detalles()}")
        print(f" -> Éxito: {s3.obtener_detalles()}")
    except SoftwareFJError as e:
        print(f" -> Error: {e}")

    # [Operación 8] Reserva exitosa de sala con descuento e IVA
    try:
        print("\n[Op 8] Procesando reserva de sala con 10% descuento + IVA...")
        r1 = gestor_reservas.crear_reserva(
            "RES-101", "1020304050", "SR-01", duracion=4, descuento=0.10, incluir_impuesto=True
        )
        print(f" -> Éxito: {r1.id_reserva} | Total: ${r1.costo_total} | Estado: {r1.estado}")
    except SoftwareFJError as e:
        print(f" -> Error: {e}")

    # [Operación 9] Reserva fallida por duración negativa, aqui se prueban 2 exepciones al tiempo
    try:
        print("\n[Op 9] Intentando reserva con duración negativa exepciones concatenadas...")
        gestor_reservas.crear_reserva("RES-102", "1020304050", "SR-01", duracion=-2)
    except ReservaInvalidaError as rie:
        print(f" -> Excepción encadenada capturada: {rie}")

    # [Operación 10] Reserva exitosa de alquiler de equipos con seguro adicional
    try:
        print("\n[Op 10] Procesando reserva de alquiler de 3 equipos por 2 días con seguro...")
        r2 = gestor_reservas.crear_reserva(
            "RES-103", "1020304050", "EQ-02", duracion=2, unidades=3, seguro=True
        )
        print(f" -> Éxito: {r2.id_reserva} | Total: ${r2.costo_total} | Estado: {r2.estado}")
    except SoftwareFJError as e:
        print(f" -> Error: {e}")

    # [Operación 11] Reserva exitosa de asesoría nivel Experto
    try:
        print("\n[Op 11] Procesando reserva de asesoría nivel Experto...")
        r3 = gestor_reservas.crear_reserva("RES-104", "1020304050", "AS-01", duracion=3, nivel="Experto")
        print(f" -> Éxito: {r3.id_reserva} | Total: ${r3.costo_total} | Estado: {r3.estado}")
    except SoftwareFJError as e:
        print(f" -> Error: {e}")

    # [Operación 12] Cancelación válida seguida de intento inválido de doble cancelación
    try:
        print("\n[Op 12] Cancelando reserva RES-101 y probando doble cancelación...")
        cancelada = gestor_reservas.cancelar_reserva("RES-101")
        print(f" -> Éxito: Reserva {cancelada.id_reserva} ahora está {cancelada.estado}")
        gestor_reservas.cancelar_reserva("RES-101")  # Segundo intento debe fallar
    except ReservaInvalidaError as rie:
        print(f" -> Doble cancelación bloqueada correctamente: {rie}")
        logger.warning(f"Op 12 controlada: {rie}")

    # 3. Reporte final de los objetos reales almacenados en las colecciones en memoria
    print("\n=== ESTADO FINAL DE LOS REPOSITORIOS EN MEMORIA ===")
    print(
        f"Totales registrados -> {len(repo_clientes.listar_todos())} clientes | "
        f"{len(repo_servicios.listar_todos())} servicios | {len(repo_reservas.listar_todos())} reservas"
    )

    print("\n--- Clientes registrados ---")
    for cliente in repo_clientes.listar_todos():
        print(f" * {cliente.obtener_detalles()}")

    print("\n--- Catálogo de servicios disponibles ---")
    for servicio in repo_servicios.listar_todos():
        print(f" * {servicio.obtener_detalles()}")

    print("\n--- Reservas procesadas ---")
    for reserva in repo_reservas.listar_todos():
        print(
            f" * Reserva {reserva.id_reserva} | Cliente: {reserva.cliente.nombre} | "
            f"Servicio: {reserva.servicio.nombre} | Estado: {reserva.estado} | Total: ${reserva.costo_total}"
        )

    logger.info("-FIN DE SESIÓN DE SIMULACIÓN-")


if __name__ == "__main__":
    main()