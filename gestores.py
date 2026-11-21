"""
Módulo: gestores.py
Responsable: Erickson castillio garcia
Descripción: Capa de lógica de negocio que orquesta repositorios, fábricas y validaciones.
version 1.0
"""

import logging  # Módulo de logging centralizado
from entidades import Cliente  # Entidad Cliente
from excepciones import (  # Excepciones personalizadas del dominio
    ClienteInvalidoError,
    ReservaInvalidaError,
    ServicioNoDisponibleError,
)
from repositorios import ClienteRepositorio, ReservaRepositorio, ServicioRepositorio  # Repositorios
from reserva import Reserva  # Entidad Reserva
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala, Servicio  # Servicios

logger = logging.getLogger("SoftwareFJ")  # Logger configurado del sistema


class GestorClientes:
    """Gestiona el registro y consulta de clientes en el sistema."""

    def __init__(self, repo: ClienteRepositorio):
        self.repo = repo  # Inyección del repositorio de clientes

    def registrar_cliente(self, cedula: str, nombre: str, email: str, telefono: str) -> Cliente:
        """Crea un objeto Cliente validado y lo almacena en el repositorio evitando duplicados."""
        cliente = Cliente(cedula, nombre, email, telefono)  # Valida datos en el constructor
        try:
            self.repo.agregar(cliente)  # aqui se intenta guardar en la lista interna
        except ValueError as ve:
            # Encadena error de duplicado a ClienteInvalidoError
            logger.warning(f"Intento de registro duplicado para cédula {cedula}")
            raise ClienteInvalidoError(f"No se pudo registrar el cliente: {ve}") from ve
        logger.info(f"Cliente registrado correctamente: {cliente.obtener_detalles()}")
        return cliente  # Retorna el objeto creado


class GestorServicios:
    """Gestiona la creación polimórfica y almacenamiento del catálogo de servicios."""

    def __init__(self, repo: ServicioRepositorio):
        self.repo = repo  # Inyección del repositorio de servicios

    def crear_servicio(self, tipo: str, **kwargs) -> Servicio:
        """Instancia el servicio especializado según 'tipo' y lo registra en memoria."""
        tipo_norm = tipo.strip().lower()  # Normaliza el tipo de servicio recibido
        try:
            # Fábrica de subclases de Servicio según el tipo solicitado
            if tipo_norm == "sala":
                servicio = ReservaSala(
                    kwargs["id_servicio"], kwargs["nombre"], kwargs["tarifa_base"], kwargs["capacidad"]
                )
            elif tipo_norm == "equipo":
                servicio = AlquilerEquipo(
                    kwargs["id_servicio"], kwargs["nombre"], kwargs["tarifa_base"], kwargs["tipo_equipo"]
                )
            elif tipo_norm == "asesoria":
                servicio = AsesoriaEspecializada(
                    kwargs["id_servicio"], kwargs["nombre"], kwargs["tarifa_base"], kwargs["area_experto"]
                )
            else:
                raise ServicioNoDisponibleError(f"Tipo de servicio no soportado: '{tipo}'.")
        except KeyError as ke:
            # Captura parámetros faltantes y los convierte en excepción del dominio
            raise ServicioNoDisponibleError(f"Falta parámetro obligatorio para el servicio: {ke}") from ke

        try:
            self.repo.agregar(servicio)  # Almacena el servicio en el repositorio
        except ValueError as ve:
            raise ServicioNoDisponibleError(f"Servicio duplicado: {ve}") from ve

        logger.info(f"Servicio creado exitosamente: {servicio.obtener_detalles()}")
        return servicio  # Retorna la instancia especializada


class GestorReservas:
    """Orquesta la creación, confirmación y cancelación de reservas."""

    def __init__(
        self,
        repo_reservas: ReservaRepositorio,
        repo_clientes: ClienteRepositorio,
        repo_servicios: ServicioRepositorio,
    ):
        self.repo = repo_reservas  # Repositorio de reservas
        self.repo_clientes = repo_clientes  # Repositorio de clientes para validación cruzada
        self.repo_servicios = repo_servicios  # Repositorio de servicios para validación cruzada

    def crear_reserva(
        self, id_reserva: str, cedula: str, id_servicio: str, duracion: int, **opciones
    ) -> Reserva:
        """Busca cliente y servicio, crea la reserva, la confirma y la guarda si es válida."""
        cliente = self.repo_clientes.buscar_por_id(cedula)  # Busca el cliente por cédula
        if cliente is None:  # Valida existencia del cliente
            raise ReservaInvalidaError(f"No existe ningún cliente registrado con cédula '{cedula}'.")

        servicio = self.repo_servicios.buscar_por_id(id_servicio)  # Busca el servicio por ID
        if servicio is None:  # Valida existencia del servicio
            raise ReservaInvalidaError(f"No existe ningún servicio registrado con ID '{id_servicio}'.")

        if self.repo.existe(id_reserva):  # Valida que el ID de reserva no esté repetido
            raise ReservaInvalidaError(f"Ya existe una reserva con el ID '{id_reserva}'.")

        reserva = Reserva(id_reserva, cliente, servicio, duracion)  # Instancia la reserva
        reserva.confirmar(**opciones)  # Ejecuta confirmación con try/except/else/finally
        self.repo.agregar(reserva)  # Guarda la reserva confirmada en memoria
        return reserva  # Retorna la reserva procesada

    def cancelar_reserva(self, id_reserva: str) -> Reserva:
        """Localiza una reserva existente y ejecuta su cancelación controlada."""
        reserva = self.repo.buscar_por_id(id_reserva)  # Busca la reserva en el repositorio
        if reserva is None:  # Valida que exista antes de cancelar
            raise ReservaInvalidaError(f"No se encontró la reserva con ID '{id_reserva}'.")
        reserva.cancelar()  # Ejecuta el cambio de estado
        return reserva  # Retorna la reserva actualizada