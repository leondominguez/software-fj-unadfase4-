"""
Módulo: logger_config.py
Responsable: Erickson castillio garcia
Descripción: Configuración central de logs archivo DEBUG y consola INFO.
version 1.0
"""

import logging  # usamos la biblioteca estandar para manejo logs
import os  # Biblioteca para gestión de rutas y directorios dentro del sistema


def configurar_logger(nombre: str = "SoftwareFJ") -> logging.Logger:
    """Configura y devuelve una instancia única del logger del sistema."""
    os.makedirs("logs", exist_ok=True)  # Crea la carpeta 'logs' si no existe

    logger = logging.getLogger(nombre)  # busca o crea el logger con el nombre indicado arriba
    if logger.handlers:  # Evita generar manejadores duplicados si la función se llama varias veces
        return logger

    logger.setLevel(logging.DEBUG)  # logger minimo para todos los eventos.

    # 1. Handler para archivo: persiste todos los eventos desde DEBUG O hasta CRITICOS
    file_handler = logging.FileHandler(
        "logs/software_fj.log", mode="a", encoding="utf-8"   ## se traza la ruta y se codifica en utf
    )
    file_handler.setLevel(logging.DEBUG)  # Nivel de detalle completo para auditoría en archivo

    # 2. Handler para consola: muestra en pantalla unicamente eventos informativos o INFO o superiores
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Evita saturar la terminal con mensajes DEBUG

    # 3. Formato de fecha, nombre de logs, severidad y mensaje
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)  # Aplica el formato al archivo de log
    console_handler.setFormatter(formatter)  # Aplica el formato a la salida de consola

    # 4. Registra ambos manejadores o handler en el logger principal
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger  # Retorna el logger listo para usarse en cualquier modulo