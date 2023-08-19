import os
import logging
from PIL import Image
from ContentType import ContentType

DATA_SIZE_BYTES = 4
MESSAGE_CONTENT_SIZE = 1 # how many bytes is used to encode ContentType enum value

log = logging.getLogger('Generator')


def string_generator(message: str) -> int:
    """Generates bits from message starting from the least significant bit.
    Embeds size of message into first 4 bytes

    Args:
        message (string): message

    Yields:
        Iterator[int]: bits
    """
    log.info('generating string')
    
    message = bytes(message, 'utf-8')
    return bytes_generator(message, ContentType.STRING)
            
            
def bytes_generator(data: bytes, contentType: ContentType) -> int:
    """Generates bits from data starting from the least significant bit.
    Embeds size of data into first 4 bytes

    Args:
        data (bytes): message
        contentType (ContentType): content type of what's hidden inside bites - metadata for decoding

    Yields:
        Iterator[int]: bits
    """
    log.info('generating bytes')
    
    size = len(data)
    sizeByte = size.to_bytes(DATA_SIZE_BYTES, 'big')
    contentTypeByte = contentType.value.to_bytes(MESSAGE_CONTENT_SIZE, 'big')
    
    log.info(f'message size: {size}, message content {contentType}')


    for byte in sizeByte + contentTypeByte + data:
        for i in range(8):
            yield (byte >> i) & 1
    
            
def file_generator(path: str) -> int:
    """Generates bits from file starting from the least significant bit.

    Args:
        path (str): path to the file

    Yields:
        Iterator[int]: bits
    """
    inputFileSize = os.path.getsize(path)
    sizeByte = os.path.getsize(path).to_bytes(DATA_SIZE_BYTES, 'big')
    contentType = ContentType.FILE
    contentTypeByte = contentType.value.to_bytes(MESSAGE_CONTENT_SIZE, 'big')

    log.info(f'file size: {inputFileSize}, message content {contentType}')
    
    file = open(path, "rb")

    # metadata
    for byte in sizeByte + contentTypeByte:
        for i in range(8):
            yield (byte >> i) & 1

    # file content
    byte = file.read(1)
    while byte:
        for i in range(8):
            yield (byte[0] >> i) & 1
        byte = file.read(1)
      
      
def hidden_bits_generator(image: Image.Image) -> int:
    """Generates hidden bites from image that contains hidden message

    Args:
        image (pillow Image): image containing hidden message

    Yields:
        Iterator[int]: bits
    """
    width, height = image.size
    
    for y in range(height):
        for x in range(width):
            pixel = image.getpixel((x, y))
            yield pixel[0] & 1
            yield pixel[1] & 1
            yield pixel[2] & 1
