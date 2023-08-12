import logging.config
from service.EmbedService import EmbedService
from generators import stringGenerator



logging.config.fileConfig("logger.conf")

embedService = EmbedService.get_instance()

generator = stringGenerator("ah")

embedService.embed_bytes("images/leafs.jpg", "images/output.jpg", generator)