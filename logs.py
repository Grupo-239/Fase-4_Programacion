import logging

logging.basicConfig(
    filename="sistema.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def registrar_error(mensaje):
    logging.error(mensaje)

def registrar_evento(mensaje):
    logging.info(mensaje)