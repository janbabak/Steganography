# import logging
# from generators.AbstractGenerator import AbstractGenerator

# class StringGenerator(AbstractGenerator):
#     """Generate data to embed from string
#     """
    
#     def __init__(self, message):
#         """constructor

#         Args:
#             message (string): message to be generated
#         """
#         self._message = bytes(message, 'utf-8')
#         self._log = logging.getLogger('StringGenerator')
#         self._log.info("created")
        
    
#     def get_generator(self) -> int:
#         """Generates bits from message string (starting from the leas significant bit), embeds the
#         length of the message (in bytes) before it

#         Yields:
#             int: bit
#         """
#         # sizeAndMessage = self.get_size().to_bytes(self.DATA_SIZE_BYTES, 'big') + self._message
            
#         # for byte in self._message:
#         #     for i in range(8):
#         #         yield (byte >> i) & 1
                    
#         def generator(message, size):
#             print("generator")
#             sizeAndMessage = size.to_bytes(self.DATA_SIZE_BYTES, 'big') + message
            
#             for byte in sizeAndMessage:
#                 for i in range(8):
#                     yield (byte >> i) & 1
                    
#         return generator(self._message, self.get_size())
    
    
                

#     def get_size(self) -> int:
#         """Get size of generated message

#         Returns:
#             int: number of bytes of message
#         """
#         return len(self._message)
DATA_SIZE_BYTES = 4

def stringGenerator(message):
    message = bytes(message, 'utf-8')
    size = len(message).to_bytes(DATA_SIZE_BYTES, 'big')

    for byte in size + message:
        for i in range(8):
            yield (byte >> i) & 1
                    