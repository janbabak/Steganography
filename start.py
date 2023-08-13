import logging.config
from service.EmbedService import EmbedService
from service.EncryptService import EncryptService
from generators import bytes_generator
from generators import string_generator


logging.config.fileConfig('logger.conf')
pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)


embedService = EmbedService.get_instance()
encryptService = EncryptService.get_instance()

message = 'What have you been up to?'
inputFilePath = 'images/leafs.jpg'
outputFilePath = 'images/output.png'
secret = '095klljmlkfj90dsf90sdf0s'

encrypted = encryptService.encrypt_string(message, secret)
generator = bytes_generator(encrypted)
embedService.embed_bytes(inputFilePath, outputFilePath, generator)
retrievedMessage = embedService.get_embedded_message(outputFilePath)
plainText = encryptService.decrypt_string(retrievedMessage, secret)

logging.info(f'hidden message is: {plainText}')

assert(message == plainText)