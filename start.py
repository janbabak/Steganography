import logging.config
from service.EmbedService import EmbedService

logging.config.fileConfig('logger.conf')
pil_logger = logging.getLogger('PIL')
pil_logger.setLevel(logging.INFO)


embedService = EmbedService.get_instance()

# message = 'What have you been up to?'
inputFilePath = 'images/christmas.jpg'
outputFilePath = 'images/output.png'

# embed string
embedService.embed_string("cau pico.", inputFilePath, outputFilePath)
embedService.get_embedded_message(outputFilePath)

# embed image
# embedService.embed_file('images/leafs.jpg', inputFilePath, outputFilePath)
# embedService.get_embedded_message(outputFilePath, 'images/message.png')