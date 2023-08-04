from service.EncryptService import EncryptService
import logging.config

logging.config.fileConfig("logger.conf")

secret = "secret key" # 16 bytes

encryptService = EncryptService.get_instance()

encrypted, iv = encryptService.encrypt_file("file", secret)

decrypted = encryptService.decrypt_file(encrypted, secret, iv)