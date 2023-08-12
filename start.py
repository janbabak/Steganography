import logging.config
from service.EmbedService import EmbedService
from generators import string_generator


logging.config.fileConfig("logger.conf")
pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)


embedService = EmbedService.get_instance()

generator = string_generator("ahoj jak je, toto je schovana zprava uvnitr obrazku")

embedService.embed_bytes("images/leafs.jpg", "images/output.png", generator)

message = embedService.get_embedded_message("images/output.png")

logging.info(f"hidden message is {message}")