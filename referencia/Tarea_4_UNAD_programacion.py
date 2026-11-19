
# Tarea 4 
# by: Jhon Alex Jaramillo Erazo 
# grupo: 213023_341
# Participantes: Jhon Alex Jaramillo 

# primero importamos ABC, abstractmethod, logging y datetime 
from abc import ABC, abstractmethod
import logging
import datetime

# vamos a hacer la configuracion del sistema de registros o logs 
logging.basicConfig(  
    filename='sistema_registros_tarea4.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    encoding='utf-8'
)
# creamos las excepciones personalizadas y encadenamiento
class SoftwareFJError(Exception):
    """Excepción principal para la gestion de los errores del sistema Software FJ."""
    pass
class ClienteInvalidoError(SoftwareFJError):    
    """Se lanza cuando los datos de un cliente no son válidos."""
    pass
class ServicioNoDisponibleError(SoftwareFJError):
    """Se genera cuando un servicio no está disponible o tiene parámetros erróneos."""
    pass
class ReservaInvalidaError(SoftwareFJError):
    """Se genera cuando ocurre un error como que la información del cliente presenta inconsistencias."""
    pass
#  crearemos la clase abstracta 
class EntidadSistema(ABC):
    """Clase abstracta que define las características comunes de las entidades del sistema"""
    
    @abstractmethod
    def obtener_detalles(self) -> str:
        pass
# creamos la clase cliente para manejo y validacion de datos
class Cliente(EntidadSistema):
    def __init__(self, cedula: str, nombre: str, email: str, telefono: str):
        self.cedula = cedula
        self.nombre = nombre
        self.email = email
        self.telefono = telefono
    # Usamos: Getter y Setter para la validacion de datos.
    # Getter (Permite leer de forma segura el valor oculto almacenado en "cedula") y 
    # Setter (Se activa automáticamente cada vez que intentamos asignar o cambiar la cédula) con validación estricta para la cédula
    @property
    def cedula(self) -> str:
        return self._cedula

    @cedula.setter
    def cedula(self, valor: str):
        if not valor or not valor.isdigit() or len(valor) < 7:
            raise ClienteInvalidoError(f"Cédula inválida ('{valor}'). Debe contener solo números y al menos 7 dígitos.")
        self._cedula = valor

    # validacion para el correo electrónico
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
            raise ClienteInvalidoError(f"El nombre del cliente ('{valor}') es demasiado corto o esta vacío.")
        self._nombre = valor
        
    # validacion del nombre y telefono
    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not valor or not valor.isdigit():
            raise ClienteInvalidoError(f"Teléfono inválido ('{valor}').")
        self._telefono = valor

    # el metodo obligatorio de la abstraccion
    def obtener_detalles(self) -> str:
        return f"Cliente: {self.nombre} | Cédula: {self.cedula} | Email: {self.email}"
    
#  creamos la clase abstracta servicio 
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
            raise ServicioNoDisponibleError(f"La tarifa base debe ser mayor a 0. Valor recibido: {valor}")
        self._tarifa_base = valor

    @abstractmethod
    def calcular_costo(self, *args, **kwargs) -> float:
        """Método abstracto que implementa polimorfismo en los servicios."""
        pass
    
# servicios especializados (herencia)
# creamos la clase "ReservaSala"
class ReservaSala(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, capacidad: int):
        super().__init__(id_servicio, nombre, tarifa_base)
        self.capacidad = capacidad

    # uso de parametros opcionales (polimorfismo y sobrecarga) para calcular los costos
    def calcular_costo(self, horas: int, descuento: float = 0.0, incluir_impuesto: bool = True) -> float:
        if horas <= 0:
            raise ValueError("Las horas de reserva de sala deben ser mayores a 0.")
        
        subtotal = self.tarifa_base * horas
        monto_con_descuento = subtotal * (1 - descuento)
        
        if incluir_impuesto:
            total = monto_con_descuento * 1.19  # IVA 19%
        else:
            total = monto_con_descuento
        return round(total, 2)

    def obtener_detalles(self) -> str:
        return f"[Sala] ID: {self.id_servicio} - {self.nombre} (Capacidad: {self.capacidad} personas) | Tarifa/h: ${self.tarifa_base}"

# creamos la clase "AlquilerEquipo"
class AlquilerEquipo(Servicio):
    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, tipo_equipo: str):
        super().__init__(id_servicio, nombre, tarifa_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, cantidad_unidades: int, dias: int, seguro_adicional: bool = False) -> float:
        if cantidad_unidades <= 0 or dias <= 0:
            raise ValueError("La cantidad de unidades y días deben ser mayores a 0.")
        
        costo_base = self.tarifa_base * cantidad_unidades * dias
        adicional = 50.0 * cantidad_unidades if seguro_adicional else 0.0
        return round(costo_base + adicional, 2)

    def obtener_detalles(self) -> str:
        return f"[Equipo] ID: {self.id_servicio} - {self.nombre} ({self.tipo_equipo}) | Tarifa base: ${self.tarifa_base}"

# creamos la clase "AsesoriaEspecializada"
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
        return f"[Asesoría] ID: {self.id_servicio} - {self.nombre} (Área: {self.area_experto}) | Tarifa/h: ${self.tarifa_base}"


#  creamos la clase "Reserva" vinculada al objeto cliente o  servicio
class Reserva:
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "Pendiente"
        self.costo_total = 0.0
    # metodo "confirmar" 
    def confirmar(self, *args, **kwargs):
        """Confirma la reserva calculando su costo con manejo avanzado de excepciones."""
        try:
            # Intentar calcular el costo según el tipo de servicio polimórfico
            if isinstance(self.servicio, ReservaSala):
                self.costo_total = self.servicio.calcular_costo(self.duracion, *args, **kwargs)
            elif isinstance(self.servicio, AlquilerEquipo):
             # Se asume duracion = días, unidades = 1 por defecto si no se pasa
                unidades = kwargs.get('unidades', 1)
                seguro = kwargs.get('seguro', False)
                self.costo_total = self.servicio.calcular_costo(unidades, self.duracion, seguro)
            elif isinstance(self.servicio, AsesoriaEspecializada):
                nivel = kwargs.get('nivel', 'Medio')
                self.costo_total = self.servicio.calcular_costo(self.duracion, nivel)
            else:
                raise ReservaInvalidaError("Tipo de servicio desconocido o no soportado.")
        # El Bloque "except" y el encadenamiento de excepciones
        except ValueError as ve:
            # Encadenamiento de excepciones (Exception Chaining)
            logging.error(f"Error de valor en reserva {self.id_reserva}: {ve}")
            raise ReservaInvalidaError(f"Fallo al procesar parámetros de costo para la reserva {self.id_reserva}.") from ve
        else:
            # Bloque ELSE: Se ejecuta únicamente si el try fue exitoso (es como la condicion si "try" no es entonces "else") 
            self.estado = "Confirmada"
            logging.info(f"Reserva {self.id_reserva} confirmada exitosamente con costo total de ${self.costo_total}.")
        finally:
            # Bloque FINALLY: Se ejecuta siempre, haya error o no
            logging.info(f"Finalizó el proceso de intento para la reserva {self.id_reserva}. Estado actual: {self.estado}")
    # metodo cancelar 
    def cancelar(self):
        if self.estado == "Cancelada":
            raise ReservaInvalidaError("La reserva ya se encuentra cancelada.")
        self.estado = "Cancelada"
        logging.info(f"La reserva {self.id_reserva} ha sido cancelada.")

# crearemos la simulacion de 10 personas si son "validas" o "invalidas"
# ==========================================
if __name__ == "__main__":
    print(" INICIO DE SIMULACIÓN DE OPERACIONES EN SOFTWARE FJ \n")
    logging.info("-INICIO DE SESIÓN DE SIMULACIÓN-")

    # creamos la ista para almacenar clientes y servicios simulados en memoria
    clientes_registrados = []
    servicios_disponibles = []
    reservas_realizadas = []

    # opwracion 1: registro valido de Cliente
    try:
        print("[Op 1] Registrando cliente válido...")
        c1 = Cliente("1020304050", "Ana María Gómez", "ana.gomez@mail.com", "3104567890")
        clientes_registrados.append(c1)
        print(f" -> Éxito: {c1.obtener_detalles()}")
    except SoftwareFJError as e:
        print(f" -> Error capturado: {e}")

    # operacion 2: el registro invalido de Cliente (si la cedula esta mal escrita o tiene letras)
    try:
        print("\n[Op 2] Intentando registrar cliente con cédula inválida...")
        c_invalido = Cliente("1020ABC", "Carlos Pérez", "carlos@mail.com", "3201234567")
        clientes_registrados.append(c_invalido)
    except SoftwareFJError as e:
        print(f" -> Error controlado correctamente: {e}")
        logging.warning(f"Intento fallido controlado: {e}")

    # operacion 3: Creación Válida de Servicio (Sala)
    try:
        print("\n[Op 3] Creando servicio de reserva de sala...")
        s1 = ReservaSala("SR-01", "Sala de Juntas Ejecutiva", 50.0, 15)
        servicios_disponibles.append(s1)
        print(f" -> Éxito: {s1.obtener_detalles()}")
    except SoftwareFJError as e:
        print(f" -> Error: {e}")

    # Operación 4: Intento de registro de un servicio con una tarifa base no válida
    try:
        print("\n[Op 4] Intentando crear servicio con tarifa negativa...")
        s_invalido = AlquilerEquipo("EQ-01", "Proyector 4K", -150.0, "Audiovisual")
        servicios_disponibles.append(s_invalido)
    except SoftwareFJError as e:
        print(f" -> Error controlado correctamente: {e}")
        logging.warning(f"Intento fallido controlado: {e}")

    # Operación 5: Creación Válida de Servicio de Equipos y Asesoría
    try:
        print("\n[Op 5] Creando servicios adicionales válidos...")
        s2 = AlquilerEquipo("EQ-02", "Laptop Core i7", 25.0, "Cómputo")
        s3 = AsesoriaEspecializada("AS-01", "Consultoría Arquitectura Software", 80.0, "Tecnología")
        servicios_disponibles.extend([s2, s3])
        print(f" -> Éxito: {s2.obtener_detalles()}")
        print(f" -> Éxito: {s3.obtener_detalles()}")
    except SoftwareFJError as e:
        print(f" -> Error: {e}")

    # Operación 6: Registro exitoso de reserva de sala con aplicación de descuentos e impuestos
    try:
        print("\n[Op 6] Procesando reserva exitosa de sala...")
        reserva1 = Reserva("RES-101", clientes_registrados[0], servicios_disponibles[0], duracion=4)
        reserva1.confirmar(descuento=0.10, incluir_impuesto=True) # 10% descuento + IVA
        reservas_realizadas.append(reserva1)
        print(f" -> Éxito: Reserva ID {reserva1.id_reserva} | Costo total: ${reserva1.costo_total} | Estado: {reserva1.estado}")
    except SoftwareFJError as e:
        print(f" -> Error: {e}")

    # Operación 7: Rechazo de reserva debido a una cantidad negativa de horas 
    try:
        print("\n[Op 7] Intentando procesar reserva con duración negativa (probando try/except/else/finally y encadenamiento)...")
        reserva_erronea = Reserva("RES-102", clientes_registrados[0], servicios_disponibles[0], duracion=-2)
        reserva_erronea.confirmar()
        reservas_realizadas.append(reserva_erronea)
    except ReservaInvalidaError as rie:
        print(f" -> Excepción personalizada capturada correctamente: {rie}")
    except SoftwareFJError as e:
        print(f" -> Otro error del sistema: {e}")

    # Operación 8: Reserva Exitosa de Asesoría Especializada
    try:
        print("\n[Op 8] Procesando reserva exitosa de asesoría especializada...")
        reserva2 = Reserva("RES-103", clientes_registrados[0], servicios_disponibles[2], duracion=3)
        reserva2.confirmar(nivel="Experto")
        reservas_realizadas.append(reserva2)
        print(f" -> Éxito: Reserva ID {reserva2.id_reserva} | Costo total: ${reserva2.costo_total} | Estado: {reserva2.estado}")
    except SoftwareFJError as e:
        print(f" -> Error: {e}")

    # Operación 9: Cancelacion de una reserva previamente registrada
    try:
        print("\n[Op 9] Cancelando la reserva RES-101...")
        reservas_realizadas[0].cancelar()
        print(f" -> Éxito: Reserva {reservas_realizadas[0].id_reserva} cambió su estado a: {reservas_realizadas[0].estado}")
    except SoftwareFJError as e:
        print(f" -> Error: {e}")

    # Operación 10: Intento de cancelar una reserva ya cancelada (Control de error de operación)
    try:
        print("\n[Op 10] Intentando cancelar nuevamente la misma reserva ya cancelada...")
        reservas_realizadas[0].cancelar()
    except ReservaInvalidaError as rie:
        print(f" -> Excepción controlada con éxito: {rie}")
        logging.warning(f"Operación no permitida evitada: {rie}")

    print("\n > SIMULACIÓN FINALIZADA CON ÉXITO < ")
    print("Revise el archivo 'sistema_registros_tarea4.log' para verificar el registro detallado de eventos y errores.")