import logging

DATA_SIZE_BYTES = 4

log = logging.getLogger("Generator")

def stringGenerator(message) -> int:
    """Generates bits from message starting from the leas significant bit.
    Embeds size of message into first 4 bytes

    Args:
        message (string): message

    Yields:
        int: bits
    """
    log.info("generating string")
    
    message = bytes(message, 'utf-8')
    size = len(message).to_bytes(DATA_SIZE_BYTES, 'big')

    for byte in size + message:
        for i in range(8):
            yield (byte >> i) & 1
      