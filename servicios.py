"""
Módulo: servicios.py
Responsable: Estudiante 2
Origen: Migrado del original
Descripción: Clase abstracta Servicio y tres servicios especializados.

TODO (Est. 2): unificar la firma de calcular_costo para eliminar los
isinstance en Reserva y lograr polimorfismo pleno.
"""

from abc import abstractmethod

from entidades import EntidadSistema
from excepciones import ServicioNoDisponibleError


class Servicio(EntidadSistema):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float):
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.tarifa_base = tarifa_base

    @property
    def tarifa_base(self) -> float:
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float):
        if valor <= 0:
            raise ServicioNoDisponibleError(
                f"La tarifa base debe ser mayor a 0. Valor recibido: {valor}"
            )
        self._tarifa_base = valor

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Método abstracto que implementa polimorfismo en los servicios."""
        ...


class ReservaSala(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad: int):
        super().__init__(id_servicio, nombre, tarifa_base)
        self.capacidad = capacidad

    def calcular_costo(
        self, horas: int, descuento: float = 0.0, incluir_impuesto: bool = True
    ) -> float:
        if horas <= 0:
            raise ValueError("Las horas de reserva de sala deben ser mayores a 0.")
        subtotal = self.tarifa_base * horas
        monto_con_descuento = subtotal * (1 - descuento)
        total = monto_con_descuento * 1.19 if incluir_impuesto else monto_con_descuento
        return round(total, 2)

    def obtener_detalles(self) -> str:
        return (
            f"[Sala] ID: {self.id_servicio} - {self.nombre} "
            f"(Capacidad: {self.capacidad} personas) | Tarifa/h: ${self.tarifa_base}"
        )


class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, tipo_equipo: str):
        super().__init__(id_servicio, nombre, tarifa_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(
        self, cantidad_unidades: int, dias: int, seguro_adicional: bool = False
    ) -> float:
        if cantidad_unidades <= 0 or dias <= 0:
            raise ValueError("La cantidad de unidades y días deben ser mayores a 0.")
        costo_base = self.tarifa_base * cantidad_unidades * dias
        adicional = 50.0 * cantidad_unidades if seguro_adicional else 0.0
        return round(costo_base + adicional, 2)

    def obtener_detalles(self) -> str:
        return (
            f"[Equipo] ID: {self.id_servicio} - {self.nombre} "
            f"({self.tipo_equipo}) | Tarifa base: ${self.tarifa_base}"
        )


class AsesoriaEspecializada(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, area_experto: str):
        super().__init__(id_servicio, nombre, tarifa_base)
        self.area_experto = area_experto

    def calcular_costo(self, horas: int, nivel_complejidad: str = "Medio") -> float:
        if horas <= 0:
            raise ValueError("Las horas de asesoría deben ser mayores a 0.")
        multiplicador = 1.0
        if nivel_complejidad.lower() == "alto":
            multiplicador = 1.5
        elif nivel_complejidad.lower() == "experto":
            multiplicador = 2.0
        return round(self.tarifa_base * horas * multiplicador, 2)

    def obtener_detalles(self) -> str:
        return (
            f"[Asesoría] ID: {self.id_servicio} - {self.nombre} "
            f"(Área: {self.area_experto}) | Tarifa/h: ${self.tarifa_base}"
        )