import logging.config
from service.EmbedService import EmbedService
from service.EncryptService import EncryptService
from generators import string_generator


logging.config.fileConfig('logger.conf')
pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)


embedService = EmbedService.get_instance()

generator = string_generator('Ahoj jak je, toto je schovana zprava uvnitr obrazku!')

embedService.embed_bytes('images/leafs.jpg', 'images/output.png', generator)

message = embedService.get_embedded_message('images/output.png')

logging.info(f'hidden message is: {message}')

encryptService = EncryptService.get_instance()

encrypted = encryptService.encrypt_string("What have you been up to?", "12345")


plainText = encryptService.decrypt_string(encrypted, "12345")

print(plainText)