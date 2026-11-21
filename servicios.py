"""
Módulo: servicios.py
Responsable: jhon alex jaramillo
Descripción: Clase abstracta Servicio y tres servicios especializados con polimorfismo pleno.
version 1.0
"""

from abc import abstractmethod  # para definir los métodos abstractos obligatorios
from entidades import EntidadSistema  # Clase base abstracta del sistema
from excepciones import ServicioNoDisponibleError  # importacion de la clase de exepciones personalizada para los errores de servicio


class Servicio(EntidadSistema):
    """Clase abstracta que representa cualquier servicio ofrecido por Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float):
        if not id_servicio or not id_servicio.strip():  # Valida que el ID no esté vacío 
            raise ServicioNoDisponibleError("El ID del servicio no puede estar vacío.")
        if not nombre or len(nombre.strip()) < 3:  # Valida longitud mínima del nombre
            raise ServicioNoDisponibleError(f"Nombre de servicio inválido: '{nombre}'.")
        self.id_servicio = id_servicio.strip()  # Asigna el ID sin datos basura 
        self.nombre = nombre.strip()  #  limmpia la cadena 
        self.tarifa_base = tarifa_base  # Invoca el setter de tarifa_base para validar

    @property
    def tarifa_base(self) -> float:
        """Retorna la tarifa base encapsulada del servicio."""
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float):
        """Valida que la tarifa base sea estrictamente mayor a cero."""
        if valor <= 0:
            raise ServicioNoDisponibleError(
                f"La tarifa base debe ser mayor a 0. Valor recibido: {valor}"
            )
        self._tarifa_base = float(valor)  # Almacena la tarifa convertida a flotante

    @abstractmethod
    def calcular_costo(self, duracion: int, **kwargs) -> float:
        """Método polimórfico unificado que cada subclase implementa según sus reglas."""
        ...


class ReservaSala(Servicio):
    """Servicio especializado para alquiler de salas por horas."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad: int):
        super().__init__(id_servicio, nombre, tarifa_base)  # Inicializa los atributos heredados
        if capacidad <= 0:  # Valida que la capacidad de personas sea positiva
            raise ServicioNoDisponibleError(
                f"La capacidad de la sala debe ser mayor a 0: {capacidad}"
            )
        self.capacidad = capacidad  # Guarda la capacidad máxima de la sala

    def calcular_costo(self, duracion: int, **kwargs) -> float:
        """Calcula costo por horas con descuento e impuesto IVA opcionales (sobrecarga vía kwargs)."""
        if duracion <= 0:  # Valida que las horas solicitadas sean positivas
            raise ValueError("Las horas de reserva de sala deben ser mayores a 0.")
        descuento = float(kwargs.get("descuento", 0.0))  # Obtiene porcentaje de descuento (0.0 a 0.99)
        incluir_impuesto = bool(kwargs.get("incluir_impuesto", True))  # se Define si aplica IVA del 19%
        if not (0.0 <= descuento < 1.0):  # se Valida rango lógico del descuento
            raise ValueError(f"El descuento debe estar entre 0 y 0.99. Recibido: {descuento}")
        subtotal = self.tarifa_base * duracion  # se Calcula tarifa base por cantidad de horas
        monto_con_descuento = subtotal * (1 - descuento)  # se Aplica el descuento al subtotal
        total = monto_con_descuento * 1.19 if incluir_impuesto else monto_con_descuento  # Aplica IVA 19%
        return round(total, 2)  # Retorna el valor redondeado a 2 decimales

    def obtener_detalles(self) -> str:
        """Implementa el método abstracto para describir la sala."""
        return (
            f"[Sala] ID: {self.id_servicio} - {self.nombre} "
            f"(Capacidad: {self.capacidad} personas) | Tarifa/h: ${self.tarifa_base}"
        )


class AlquilerEquipo(Servicio):
    """Servicio especializado para alquiler de equipos tecnológicos por días."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, tipo_equipo: str):
        super().__init__(id_servicio, nombre, tarifa_base)  # Inicializa los atributos base
        if not tipo_equipo or not tipo_equipo.strip():  # Valida que se indique la categoría de equipo
            raise ServicioNoDisponibleError("Debe especificar el tipo de equipo.")
        self.tipo_equipo = tipo_equipo.strip()  # Guarda la categoría del equipo

    def calcular_costo(self, duracion: int, **kwargs) -> float:
        """Calcula costo por días, cantidad de unidades y seguro adicional opcional."""
        unidades = int(kwargs.get("unidades", 1))  # Cantidad de equipos a alquilar (por defecto 1)
        seguro_adicional = bool(kwargs.get("seguro", False))  # Seguro opcional por unidad
        if unidades <= 0 or duracion <= 0:  # Valida los valores estrictamente positivos
            raise ValueError("La cantidad de unidades y días deben ser mayores a 0.")
        costo_base = self.tarifa_base * unidades * duracion  # Calcula la tarifa diaria total
        adicional = 50.0 * unidades if seguro_adicional else 0.0  # Suma $50 por unidad si hay seguro
        return round(costo_base + adicional, 2)  # Retorna el costo final redondeado

    def obtener_detalles(self) -> str:
        """Implementa el método abstracto para describir el equipo."""
        return (
            f"[Equipo] ID: {self.id_servicio} - {self.nombre} "
            f"({self.tipo_equipo}) | Tarifa/día: ${self.tarifa_base}"
        )


class AsesoriaEspecializada(Servicio):
    """Servicio especializado para consultoría técnica según nivel de complejidad."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, area_experto: str):
        super().__init__(id_servicio, nombre, tarifa_base)  # Inicializa los atributos base
        if not area_experto or not area_experto.strip():  # Valida que exista un área de especialidad
            raise ServicioNoDisponibleError("Debe especificar el área del experto.")
        self.area_experto = area_experto.strip()  # Guarda el área de conocimiento

    def calcular_costo(self, duracion: int, **kwargs) -> float:
        """Calcula costo por horas aplicando multiplicador según nivel de complejidad."""
        if duracion <= 0:  # Valida que las horas sean mayores a cero
            raise ValueError("Las horas de asesoría deben ser mayores a 0.")
        nivel = str(kwargs.get("nivel", "Medio")).lower()  # Obtiene el nivel de complejidad
        multiplicadores = {"bajo": 0.9, "medio": 1.0, "alto": 1.5, "experto": 2.0}  # Mapa de las tarifas
        if nivel not in multiplicadores:  # Valida que el nivel exista en el catálogo
            raise ValueError(f"Nivel de complejidad inválido: '{nivel}'.")
        return round(self.tarifa_base * duracion * multiplicadores[nivel], 2)  # Calcula y redondea

    def obtener_detalles(self) -> str:
        """Implementa el método abstracto para describir la asesoría."""
        return (
            f"[Asesoría] ID: {self.id_servicio} - {self.nombre} "
            f"(Área: {self.area_experto}) | Tarifa/h: ${self.tarifa_base}"
        )