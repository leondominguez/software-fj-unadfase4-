"""
Módulo: excepciones.py
Responsable: Estudiante 1
Origen: Migrado del original
Descripción: Excepciones personalizadas del sistema Software FJ.
"""


class SoftwareFJError(Exception):
    """Excepción base para todos los errores del sistema Software FJ."""


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no son válidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza cuando un servicio no está disponible o tiene parámetros inválidos."""


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando una reserva no puede procesarse, confirmarse o cancelarse."""