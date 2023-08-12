import logging


class StringIterator:
    
    def __init__(self, message):
        """constructor

        Args:
            message (string): message to be generated
        """
        self._message = bytes(message, 'utf-8')
        self._log = logging.getLogger('StringIterator')
        self._log.info("created")
    
    
    def __iter__(self):
        return self
    
    
    def __next__(self):
        if not self._message:
            raise StopIteration
        
        bit = self._message[0]
        self._message = self._message[1:]
        return bit
    
    
    def get_size(self) -> int:
        """Get size of generated message

        Returns:
            int: number of bytes of message
        """
        return len(self._message)