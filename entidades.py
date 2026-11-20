"""
Módulo: entidades.py
Responsable: Leon Dominguez
Descripción: Clase abstracta EntidadSistema y clase Cliente con encapsulación y validaciones.
version: 1.0
"""

from abc import ABC, abstractmethod  # Herramientas las para clases y métodos abstractos
from excepciones import ClienteInvalidoError  # Excepciónes personalizadas para los datos de cliente importadas desde el módulo excepciones.py


class EntidadSistema(ABC):
    """Clase abstracta base que define el contrato común para las entidades del sistema."""

    @abstractmethod
    def obtener_detalles(self) -> str:
        """Método obligatorio que cada entidad hija debe implementar para describirse."""
        ...


class Cliente(EntidadSistema):
    """Representa un cliente de Software FJ con validación estricta en sus atributos."""

    def __init__(self, cedula: str, nombre: str, email: str, telefono: str):
        self.cedula = cedula  # Ejecutar el setter @cedula.setter para poder  validar formato numérico
        self.nombre = nombre  # Ejecutar el setter @nombre.setter para poder validar longitud mínima
        self.email = email  # Ejecuta el setter @email.setter para poder validar estructura de correo
        self.telefono = telefono  # Ejecutar el setter @telefono.setter para poder validar dígitos

    @property
    def cedula(self) -> str:
        """Getter que retorna la cédula encapsulada del cliente."""
        return self._cedula

    @cedula.setter
    def cedula(self, valor: str):
        """Setter que valida que la cédula contenga solo dígitos y tenga al menos 7 caracteres."""
        if not valor or not valor.isdigit() or len(valor) < 7:
            raise ClienteInvalidoError(
                f"Cédula inválida ('{valor}'). Debe contener solo números y al menos 7 dígitos."
            )
        self._cedula = valor  # Aqui se Almacena el valor validado en el atributo privado

    @property
    def email(self) -> str:
        """Getter que retorna el correo electrónico encapsulado."""
        return self._email

    @email.setter
    def email(self, valor: str):
        """Setter que verifica la presencia de '@' y '.' en el correo electrónico."""
        if not valor or "@" not in valor or "." not in valor:
            raise ClienteInvalidoError(f"Correo electrónico inválido ('{valor}').")
        self._email = valor.strip()  # Guardamos el correo sin espacios en al incio y al final.

    @property
    def nombre(self) -> str:
        """Getter que retorna el nombre completo del cliente."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        """Setter que valida que el nombre no esté vacío y tenga mínimo 3 caracteres."""
        if not valor or len(valor.strip()) < 3:
            raise ClienteInvalidoError(
                f"El nombre del cliente ('{valor}') es demasiado corto o está vacío."
            )
        self._nombre = valor.strip()  # Almacena el nombre limpio

    @property
    def telefono(self) -> str:
        """Getter que retorna el número telefónico del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        """Setter que exige que el teléfono esté compuesto únicamente por dígitos."""
        if not valor or not valor.isdigit():
            raise ClienteInvalidoError(f"Teléfono inválido ('{valor}').")
        self._telefono = valor  # Guarda el teléfono validado

    def obtener_detalles(self) -> str:
        """Implementa el método abstracto retornando un resumen legible del cliente."""
        return f"Cliente: {self.nombre} | Cédula: {self.cedula} | Email: {self.email}"