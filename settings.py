import logging

# Configuración del logger
logging.basicConfig(filename='log.log',
                    level=logging.DEBUG,
                    format='%(asctime)s [%(levelname)s]: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Crear un objeto logger
logger = logging.getLogger(__name__)
