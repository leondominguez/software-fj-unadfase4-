"""
Módulo: excepciones.py
Responsable: Leon Dominguez
Descripción: Jerarquía de excepciones personalizadas del sistema Software FJ.
Version: 1.0
"""


class SoftwareFJError(Exception):
    """Excepción base de la que heredan todos los errores controlados del sistema."""

    pass  # Hereda el comportamiento de Exception


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos personales o el registro de un cliente son inválidos."""

    pass  # Permite capturar los errores específicos de validación en clientes


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando un servicio no existe, está duplicado o tiene parámetros inválidos."""

    pass  # Permite aislar fallos al crear o consultar clientes


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva falla al crearse, confirmarse o cancelarse."""

    pass  # Permite manejar los errores en el proceso logico de las reservas