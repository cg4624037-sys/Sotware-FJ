import logging

# Configuracion del archivo de registro
logging.basicConfig(
    filename="logs_sistema.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

# Funcion para registrar eventos
def registrar_evento(mensaje):
    logging.info(mensaje)


# Funcion para registrar errores
def registrar_error(mensaje):
    logging.error(mensaje)