"""
Módulo: logger_config.py
Responsable: Estudiante 4
Origen: Configuración centralizada basada en la guía de la actividad
        (patrón FileHandler + StreamHandler).
Descripción: Logger con salida a archivo (DEBUG) y consola (INFO).
"""

import logging
import os


def configurar_logger(nombre: str = "SoftwareFJ") -> logging.Logger:
    """Configura y devuelve el logger del sistema (una sola vez)."""
    os.makedirs("logs", exist_ok=True)  # red de seguridad si falta la carpeta

    logger = logging.getLogger(nombre)
    if logger.handlers:  # evita duplicar handlers si se llama varias veces
        return logger

    logger.setLevel(logging.DEBUG)

    # 1. Handler para ARCHIVO: guarda todo desde DEBUG
    file_handler = logging.FileHandler(
        "logs/software_fj.log", mode="a", encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)

    # 2. Handler para CONSOLA: solo INFO o superior
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 3. Formato común
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # 4. Agregar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger