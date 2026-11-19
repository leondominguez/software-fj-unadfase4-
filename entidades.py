"""
Módulo: entidades.py
Responsable: Estudiante 1
Origen: Migrado del original
Descripción: Clase abstracta EntidadSistema y clase Cliente con encapsulación.
"""

from abc import ABC, abstractmethod

from excepciones import ClienteInvalidoError


class EntidadSistema(ABC):
    """Clase abstracta  de las entidades."""

    @abstractmethod
    def obtener_detalles(self) -> str:
        ...


class Cliente(EntidadSistema):
    def __init__(self, cedula: str, nombre: str, email: str, telefono: str):
        self.cedula = cedula
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

    @property
    def cedula(self) -> str:
        return self._cedula

    @cedula.setter
    def cedula(self, valor: str):
        if not valor or not valor.isdigit() or len(valor) < 7:
            raise ClienteInvalidoError(
                f"Cédula inválida ('{valor}'). Debe contener solo números y al menos 7 dígitos."
            )
        self._cedula = valor

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valor: str):
        if not valor or "@" not in valor or "." not in valor:
            raise ClienteInvalidoError(f"Correo electrónico inválido ('{valor}').")
        self._email = valor

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not valor or len(valor.strip()) < 3:
            raise ClienteInvalidoError(
                f"El nombre del cliente ('{valor}') es demasiado corto o está vacío."
            )
        self._nombre = valor

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not valor.isdigit():
            raise ClienteInvalidoError(f"Teléfono inválido ('{valor}').")
        self._telefono = valor

    def obtener_detalles(self) -> str:
        return f"Cliente: {self.nombre} | Cédula: {self.cedula} | Email: {self.email}"