"""
Módulo: reserva.py
Responsable: jhon alex jaramillo
Origen: Migrado del original
Descripción: Clase Reserva con confirmación y cancelación.
"""

import logging  # guarda los mensajes y errores en el log

from entidades import Cliente  # importa la clase Cliente
from excepciones import ReservaInvalidaError  # excepción propia para errores en reservas
from servicios import Servicio  # Contrato común de los servicios

logger = logging.getLogger("SoftwareFJ")  # crea o toma el logger del proyecto


class Reserva:
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        self.id_reserva = id_reserva  # guarda el código o id de la reserva
        self.cliente = cliente  # guarda el cliente que hace la reserva
        self.servicio = servicio  # guarda el objeto del servicio reservado
        self.duracion = duracion  # guarda la duración (horas o días según el servicio)
        self.estado = "Pendiente"  # toda reserva arranca como pendiente
        self.costo_total = 0.0  # empieza en 0 hasta que se confirme y calcule

    def confirmar(self, **kwargs):
        """Confirma la reserva calculando su costo con manejo avanzado de excepciones."""
        try:
            self.costo_total = self.servicio.calcular_costo(self.duracion, **kwargs)
        except ValueError as ve:  # si falla algún dato o cálculo con el ValueError
            logger.error(f"Error de valor en reserva {self.id_reserva}: {ve}")  # registra el error en el log
            raise ReservaInvalidaError(  # lanza nuestra excepción personalizada encadenando la original
                f"Fallo al procesar parámetros de costo para la reserva {self.id_reserva}."
            ) from ve
        else:  # solo entra aquí si no hubo errores en el try
            self.estado = "Confirmada"  # cambia el estado a confirmada
            logger.info(  # deja registro de que todo salió bien y muestra el total
                f"Reserva {self.id_reserva} confirmada exitosamente con costo total de ${self.costo_total}."
            )
        finally:  # se ejecuta siempre al final, haya salido bien o mal
            logger.info(
                f"Finalizó el intento de confirmación de la reserva {self.id_reserva}. "
                f"Estado actual: {self.estado}"
            )

    def cancelar(self):
        if self.estado == "Cancelada":  # evita cancelar dos veces la misma reserva
            raise ReservaInvalidaError("La reserva ya se encuentra cancelada.")
        self.estado = "Cancelada"  # cambia el estado a cancelada
        logger.info(f"La reserva {self.id_reserva} ha sido cancelada.")  # registra la cancelación en el log