from service.EncryptService import EncryptService
import logging.config

logging.config.fileConfig("logger.conf")

secret = "secret key" # 16 bytes

encryptService = EncryptService.get_instance()


encryptService.encrypt_file("./images/example-150kb.png", "./images/encrypted.out", "ahoj")
encryptService.decrypt_file("./images/encrypted.out", "./images/decrypted.png", "ahoj")