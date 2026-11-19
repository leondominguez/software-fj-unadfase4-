"""
Módulo: gestores.py
Responsable: Estudiante 4
Descripción: Lógica de negocio que orquesta repositorios y entidades.
"""

import logging

from repositorios import ClienteRepositorio, ServicioRepositorio, ReservaRepositorio

logger = logging.getLogger("SoftwareFJ")


class GestorClientes:
    def __init__(self, repo: ClienteRepositorio):
        self.repo = repo

    def registrar_cliente(self, cedula: str, nombre: str, email: str, telefono: str):
        raise NotImplementedError("Implementar")


class GestorServicios:
    def __init__(self, repo: ServicioRepositorio):
        self.repo = repo

    def crear_servicio(self, tipo: str, **kwargs):
        raise NotImplementedError("Implementar")


class GestorReservas:
    def __init__(
        self,
        repo_reservas: ReservaRepositorio,
        repo_clientes: ClienteRepositorio,
        repo_servicios: ServicioRepositorio,
    ):
        self.repo = repo_reservas
        self.repo_clientes = repo_clientes
        self.repo_servicios = repo_servicios

    def crear_reserva(
        self, id_reserva: str, cedula: str, id_servicio: str, duracion: int, **opciones
    ):
        raise NotImplementedError("Implementar")

    def cancelar_reserva(self, id_reserva: str):
        raise NotImplementedError("Implementar")