import os
import logging
from PIL import Image
from generators import *


class EmbedService:
        
    BITS_IN_BYTES = 8
    
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
            generator (generator): generates data to embed
        """
        inputImage = Image.open(inputFilePath)
        outputImage = Image.new("RGB", inputImage.size)
        
        width, height = inputImage.size
        for y in range(height):
            for x in range(width):
                pixel = inputImage.getpixel((x, y))
                outputImage.putpixel((x, y), self._embed_bites_into_pixel(pixel, generator))
                
        outputImage.save(outputFilePath,  quality=100, subsampling=0)


    def _embed_bites_into_pixel(self, pixel, generator) -> (int, int, int):
        """Embed bites into pixel

        Args:
            pixel ((int, int, int)): pixel of RGB channels
            generator (generator): generates the data to embed

        Returns:
            (int, int, int): pixel of RGB channels 
        """
        return (
            self._embed_bit_into_number(pixel[0],generator),
            self._embed_bit_into_number(pixel[1],generator),
            self._embed_bit_into_number(pixel[2],generator)
        )
        
             
    def _embed_bit_into_number(self, number, generator) -> int:
        """Embed bit to the leas significant bit of the number

        Args:
            number (int): bit is embedded to this number
            generator (generator): generates the data to embed

        Returns:
            int: _description_
        """
        try:
            bit = next(generator)
            # self._log.info(f" embedding: {bit}")
            number = (number >> 1) << 1
            return number | bit
        except StopIteration:
            return number
        
        
    def get_embedded_message(self, inputFilePath) -> str:
        """Read embedded message from file

        Args:
            inputFilePath (string): path to the input file containing embedded message

        Returns:
            string: message
        """
        inputImage = Image.open(inputFilePath)
        width, height = inputImage.size
        hiddenBitsGenerator = hidden_bits_generator(inputImage)
        messageSize = self._read_message_size(hiddenBitsGenerator)

        self._log.info(f"message size is {messageSize}")
        
        message = ""
        
        for i in range(messageSize):
            charNumber = 0
            
            for j in range(self.BITS_IN_BYTES):
                charNumber += (next(hiddenBitsGenerator) << j)
                
            message += chr(charNumber)
            
        return message
                
                
                
    def _read_message_size(self, generator) -> int:
        """Read size of embedded data (in bytes) from generator

        Args:
            generator (generator): embedded data generator

        Returns:
            int: embedded data size
        """
        size = 0
        
        for i in range(DATA_SIZE_BYTES):
            byte = 0
            for j in range(self.BITS_IN_BYTES):
                bit = next(generator) << j
                byte += bit
            
            size += byte * 2**(self.BITS_IN_BYTES * (DATA_SIZE_BYTES - (i + 1)))
            
        return size