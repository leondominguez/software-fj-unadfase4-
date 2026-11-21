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

    atributo_id: str

    def __init__(self):
        self._items: List[T] = []

    def agregar(self, item: T) -> None:
        id_ = getattr(item, self.atributo_id)
        if self.existe(id_):
            raise ValueError(f"Ya existe un elemento con ID '{id_}'.")
        self._items.append(item)

    def buscar_por_id(self, id_: str) -> Optional[T]:
        for item in self._items:
            if getattr(item, self.atributo_id) == id_:
                return item
        return None

    def listar_todos(self) -> List[T]:
        return list(self._items)

    def existe(self, id_: str) -> bool:
        return self.buscar_por_id(id_) is not None


class ClienteRepositorio(BaseRepositorio[Cliente]):
    atributo_id = "cedula"


class ServicioRepositorio(BaseRepositorio[Servicio]):
    atributo_id = "id_servicio"


class ReservaRepositorio(BaseRepositorio[Reserva]):
    atributo_id = "id_reserva"