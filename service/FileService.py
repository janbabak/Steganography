import logging
from exception.NotBytesException import NotBytesException


class FileService:
    
    _instance = None
    _log = logging.getLogger("FileService")
    
    @classmethod
    def get_instance(cls):
        """Create singleton instance

        Returns:
            FileService: singleton instance
        """
        if cls._instance == None:
            cls._instance = cls.__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Singleton has forbidden constructor

        Raises:
            RuntimeError: when this method is called, call `get_instance()` instead
        """
        raise RuntimeError('Call get_instance() instead')
    
    
    def get_file_bytes(self, filePath):
        """Read file as bytes

        Args:
            filePath (string): path to file

        Returns:
            bytes: binary content of file
        """
        self._log.info(f"Reading {filePath} file.")
        
        file = open(filePath, "rb")
        byte = file.read(1)
        content = byte
        
        while byte:
            byte = file.read(1)
            content += byte
            
        return content
    
    
    def save_bytes_to_file(self, filePath, content):
        """Save bytes to file

        Args:
            filePath (string): file path
            content (bytes): binary content of file
        """
        self._log.info(f"Saving {filePath} file")
        
        if not isinstance(content, (bytes, bytearray, memoryview)):
            raise NotBytesException
        
        file = open(filePath, "wb")
        
        file.write(content)