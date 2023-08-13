import logging
from PIL import Image

DATA_SIZE_BYTES = 4

log = logging.getLogger('Generator')

def string_generator(message: str) -> int:
    """Generates bits from message starting from the leas significant bit.
    Embeds size of message into first 4 bytes

    Args:
        message (string): message

    Yields:
        int: bits
    """
    log.info('generating string')
    
    message = bytes(message, 'utf-8')
    size = len(message).to_bytes(DATA_SIZE_BYTES, 'big')

    for byte in size + message:
        for i in range(8):
            yield (byte >> i) & 1
      
      
def hidden_bits_generator(image: Image.Image) -> int:
    """Generates hidden bites from image

    Args:
        image (pillow Image): image containing hidden message

    Yields:
        int: bits
    """
    width, height = image.size
    
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            yield pixel[0] & 1
            yield pixel[1] & 1
            yield pixel[2] & 1
