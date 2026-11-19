"""
Módulo: reserva.py
Responsable: Estudiante 3
Origen: Migrado del original
Descripción: Clase Reserva con confirmación y cancelación.

TODO (Est. 3): reemplazar los isinstance por una llamada polimórfica
única cuando Est. 2 unifique la firma de calcular_costo.
"""

import logging

from entidades import Cliente
from excepciones import ReservaInvalidaError
from servicios import Servicio, ReservaSala, AlquilerEquipo, AsesoriaEspecializada

logger = logging.getLogger("SoftwareFJ")


class Reserva:
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.costo_total = 0.0

    def confirmar(self, *args, **kwargs):
        """Confirma la reserva calculando su costo con manejo avanzado de excepciones."""
        try:
            if isinstance(self.servicio, ReservaSala):
                self.costo_total = self.servicio.calcular_costo(self.duracion, *args, **kwargs)
            elif isinstance(self.servicio, AlquilerEquipo):
                unidades = kwargs.get("unidades", 1)
                seguro = kwargs.get("seguro", False)
                self.costo_total = self.servicio.calcular_costo(unidades, self.duracion, seguro)
            elif isinstance(self.servicio, AsesoriaEspecializada):
                nivel = kwargs.get("nivel", "Medio")
                self.costo_total = self.servicio.calcular_costo(self.duracion, nivel)
            else:
                raise ReservaInvalidaError("Tipo de servicio desconocido o no soportado.")
        except ValueError as ve:
            logger.error(f"Error de valor en reserva {self.id_reserva}: {ve}")
            raise ReservaInvalidaError(
                f"Fallo al procesar parámetros de costo para la reserva {self.id_reserva}."
            ) from ve
        else:
            self.estado = "Confirmada"
            logger.info(
                f"Reserva {self.id_reserva} confirmada exitosamente con costo total de ${self.costo_total}."
            )
        finally:
            logger.info(
                f"Finalizó el intento de confirmación de la reserva {self.id_reserva}. "
                f"Estado actual: {self.estado}"
            )

    def cancelar(self):
        if self.estado == "Cancelada":
            raise ReservaInvalidaError("La reserva ya se encuentra cancelada.")
        self.estado = "Cancelada"
        logger.info(f"La reserva {self.id_reserva} ha sido cancelada.")