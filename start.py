from service.encryption import Encrypt
import logging.config

logging.config.fileConfig("logger.conf")

secret = "secret key"

# Encrypt.getInstance.encrypt_file("file", secret)

encryptService = Encrypt.get_instance()

encryptService.encrypt_file("file", secret)
