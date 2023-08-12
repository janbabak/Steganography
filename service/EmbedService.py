import os
import logging
from service.EmbedToJpgService import EmbedToJpgService


class EmbedService:
        
    _instance = None
    _log = logging.getLogger("EmbedService")
    
    
    @classmethod
    def get_instance(cls):
        """Create singleton instance

        Returns:
            EncryptService: singleton instance
        """
        if cls._instance == None:
            cls._instance = cls.__new__(cls)
        return cls._instance
    
    
    def embed_bytes(self, inputFilePath, outputFilePath, generator) -> None:
        """Embed bytes from generator to the input file

        Args:
            inputFilePath (string): path to the input file
            outputFilePath (string): path to the output file
            generator (AbstractGenerator): class responsible for generating data to embed
        """
        _, fileExtension = os.path.splitext(inputFilePath)
        
        embedToSomethingService = None
        
        if fileExtension == ".jpg" or fileExtension == ".jpeg":
            embedToSomethingService = EmbedToJpgService.get_instance()
        else:
            self._log.error(f"file type {fileExtension} not supported")
            return
        
        embedToSomethingService.embed_bytes(inputFilePath, outputFilePath, generator)
        