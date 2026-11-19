"""
Módulo: repositorios.py
Responsable: Estudiante 3
Descripción: Almacenamiento en memoria con listas internas (sin base de datos).
"""

from typing import Generic, List, Optional, TypeVar

from entidades import Cliente
from reserva import Reserva
from servicios import Servicio

T = TypeVar("T")


class BaseRepositorio(Generic[T]):
    """Repositorio genérico en memoria."""

    def __init__(self):
        self._items: List[T] = []

    def agregar(self, item: T) -> None:
        raise NotImplementedError("Implementar Estudiante 3")

    def buscar_por_id(self, id_: str) -> Optional[T]:
        raise NotImplementedError("Implementar Estudiante 3")

    def listar_todos(self) -> List[T]:
        return list(self._items)

    def existe(self, id_: str) -> bool:
        raise NotImplementedError("Implementar Estudiante 3")


class ClienteRepositorio(BaseRepositorio[Cliente]):
    ...


class ServicioRepositorio(BaseRepositorio[Servicio]):
    ...


class ReservaRepositorio(BaseRepositorio[Reserva]):
    ...