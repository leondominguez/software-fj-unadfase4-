"""
Módulo: main.py
Responsable: Estudiante 5
Descripción: Simulación de las 10 operaciones de Software FJ usando los gestores.
"""

from logger_config import configurar_logger


def main():
    logger = configurar_logger()
    logger.info("-INICIO DE SESIÓN DE SIMULACIÓN-")

    # TODO (Est. 5): reescribir las 10 operaciones del monolito original
    # usando GestorClientes, GestorServicios y GestorReservas en lugar
    # de las listas sueltas del archivo de referencia.

    logger.info("-FIN DE SESIÓN DE SIMULACIÓN-")


if __name__ == "__main__":
    main()