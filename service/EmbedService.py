import logging
import os
from PIL import Image
from generators import *
from typing import Generator
from service.EncryptService import EncryptService


class EmbedService:
        
    BITS_IN_BYTES = 8
    
    _instance = None
    _log = logging.getLogger('EmbedService')
    _encryptService = EncryptService.get_instance()
    
    
    @classmethod
    def get_instance(cls):
        """Create singleton instance

        Returns:
            EncryptService: singleton instance
        """
        if cls._instance == None:
            cls._instance = cls.__new__(cls)
        return cls._instance
    
    
    def embed_file(self, pathToFileToEmbed: str, pathToInputImage: str, pathToOutputImage: str, secret: str = '') -> None:
        """Embed file into another file.

        Args:
            pathToInputImage (str): path to the input file - message will be embedded into this file
            pathToOutputImage (str): path to the output file - file with embedded message inside
            pathToFileToEmbed (str): path to the file that you want to embed/hide
            secret (str, optional): secret password for encryption. Defaults to ''.
        """
        if not self._validate_size(pathToInputImage, pathToFileToEmbed=pathToFileToEmbed):
            self._log.error('🚨 input image is to small, embedded content can\'t fit there')
            return
        
        encryptedFileName = pathToFileToEmbed + '.encrypted'
        self._encryptService.encrypt_file(pathToFileToEmbed, encryptedFileName, secret)
        generator = file_generator(encryptedFileName)
        self._embed_bytes(pathToInputImage, pathToOutputImage, generator)
        os.remove(encryptedFileName) # remove encrypted file for fs
        
        
    def embed_string(self, plainText: str, pathToInputImage: str, pathToOutputImage: str, secret: str = '') -> None:
        """Embed string into another file.

        Args:
            plainText (str): string to embed
            pathToInputImage (str): path to the input file - message will be embedded into this file
            pathToOutputImage (str): path to the output file - file with embedded message inside
            secret (str, optional): secret password for encryption. Defaults to ''.
        """
        if not self._validate_size(pathToInputImage, plainText=plainText):
            self._log.error('🚨 input image is to small, embedded content can\'t fit there')
            return
        
        encryptedMessage = self._encryptService.encrypt_string(plainText, secret)
        generator = bytes_generator(encryptedMessage, ContentType.STRING)
        self._embed_bytes(pathToInputImage, pathToOutputImage, generator)
        
    
    def _validate_size(self, pathToInputImage: str, pathToFileToEmbed: str = None, plainText: str = None) -> bool:
        """Validate if input image is big enough to fit in the embedded content.

        Args:
            pathToInputImage (str): path to the input image - message will be embedded into this file
            pathToFileToEmbed (str, optional): path to the file to embed. Defaults to None.
            plainText (str, optional): plain text to embed. Defaults to None.

        Returns:
            bool: _description_
        """
        numberOfBytesToEmbed = 0
        
        # number of row bytes to embed
        if plainText:
            numberOfBytesToEmbed = len(plainText)
        elif pathToFileToEmbed:
            numberOfBytesToEmbed = os.path.getsize(pathToFileToEmbed)
        else:
            return False

        # number of bytes to embed after encryption
        if numberOfBytesToEmbed % EncryptService.BLOCK_SIZE != 0:
            numberOfBytesToEmbed = ((numberOfBytesToEmbed // EncryptService.BLOCK_SIZE) + 1) * EncryptService.BLOCK_SIZE

        # add bytes containing metadata
        numberOfBytesToEmbed += EncryptService.INIT_VECTOR_LENGTH
        numberOfBytesToEmbed += EncryptService.SIZE_LENGTH
        numberOfBytesToEmbed += MESSAGE_CONTENT_SIZE
        numberOfBytesToEmbed += MESSAGE_CONTENT_SIZE
        
        width, height = Image.open(pathToInputImage).size
        numberOfBytesOfInputImagePixels = width * height * 3 # 3 because of 3 color channels (R, G, B)
        
        # validation
        numberOfBitsToEmbed = numberOfBytesToEmbed * self.BITS_IN_BYTES
        self._log.info(f'number of bits to embed: {numberOfBitsToEmbed} to number of bytes of input image pixels {numberOfBytesOfInputImagePixels}')
        return numberOfBytesOfInputImagePixels > numberOfBitsToEmbed # 1 bit is embedded into one byte of input image
        
    
    def _embed_bytes(self, inputFilePath: str, outputFilePath: str, generator: Generator[int, int, None]) -> None:
        """Embed bytes from generator to the input file

        Args:
            inputFilePath (string): path to the input file
            outputFilePath (string): path to the output file
            generator (Generator[int, int, None]): generates data to embed
        """
        inputImage = Image.open(inputFilePath)
        outputImage = Image.new('RGB', inputImage.size)
        
        width, height = inputImage.size
        for y in range(height):
            for x in range(width):
                pixel = inputImage.getpixel((x, y))
                outputImage.putpixel((x, y), self._embed_bites_into_pixel(pixel, generator))
                
        outputImage.save(outputFilePath,  quality=100, subsampling=0)


    def _embed_bites_into_pixel(self, pixel: tuple[int, int, int], generator: Generator[int, str, None]) -> (int, int, int):
        """Embed bites into pixel

        Args:
            pixel ((int, int, int)): pixel of RGB channels
            generator (Generator[int, int, None]): generates the data to embed

        Returns:
            (int, int, int): pixel of RGB channels 
        """
        return (
            self._embed_bit_into_number(pixel[0],generator),
            self._embed_bit_into_number(pixel[1],generator),
            self._embed_bit_into_number(pixel[2],generator)
        )
        
             
    def _embed_bit_into_number(self, number: int, generator: Generator[int, int, None]) -> int:
        """Embed bit to the leas significant bit of the number

        Args:
            number (int): bit is embedded to this number
            generator (Generator[int, int, None]): generates the data to embed

        Returns:
            int: _description_
        """
        try:
            bit = next(generator)
            number = (number >> 1) << 1
            return number | bit
        except StopIteration:
            return number
        
        
    def get_embedded_message(self, inputFilePath: str, outputFilePath: str = '', secret: str = '') -> None:
        """Read embedded message from file and save it to file (if it's file) or display it (if it's string)

        Args:
            inputFilePath (string): path to the input file containing embedded message
            outputFilePath (string): path to the output file if the message's content type is file
        """
        inputImage = Image.open(inputFilePath)
        hiddenBitsGenerator = hidden_bits_generator(inputImage)
        messageSize, contentType = self._read_message_metadata(hiddenBitsGenerator)

        self._log.info(f' get embedded message - size: {messageSize}, contentType: {contentType}')
        
        if contentType == ContentType.STRING:
            self._show_embedded_message(messageSize, secret, hiddenBitsGenerator)
        elif contentType == ContentType.FILE:
            self._save_embedded_file(outputFilePath, messageSize, secret, hiddenBitsGenerator)
        else:
            self._log.error(f'unknown message content: {contentType}')
            
            
    def _save_embedded_file(self, outputFilePath: str, fileSize: int, secret: str, generator: Generator[int, int, None]) -> None:
        """Save and decrypt file that was embedded into image.

        Args:
            outputFilePath (str): path to the output file
            messageSize (int): message size in bytes
            secret (str): secret password for decryption
            generator (Generator[int, int, None]): hidden bits generator
        """
        encryptedFileName = outputFilePath + '.encrypted'
        encryptedFile = open(encryptedFileName, 'wb')
        for _ in range(fileSize):
            byte = 0
            for i in range(self.BITS_IN_BYTES):
                byte += (next(generator) << i)
            byte = byte.to_bytes(1, 'big')
            encryptedFile.write(byte)
        encryptedFile.close()
        
        self._encryptService.decrypt_file(encryptedFileName, outputFilePath, secret)
        os.remove(encryptedFileName) # remove encrypted file from fs
        
        self._log.info(f'embedded file saved to as {outputFilePath}')
    
    
    def _show_embedded_message(self, messageSize: int, secret: str, generator: Generator[int, int, None]) -> None:
        """Show embedded message.

        Args:
            messageSize (int): message size in bytes
            secret (str): secret password for decryption
            generator (Generator[int, int, None]): hidden bit generator
        """
        message = bytes()
        for _ in range(messageSize):
            byte = 0
            for i in range(self.BITS_IN_BYTES):
                byte += (next(generator) << i)
            message += byte.to_bytes(1, 'big')
            
        message = self._encryptService.decrypt_string(message, secret)
        
        self._log.info(f'message is: {message}')
                
                
    def _read_message_metadata(self, generator: Generator[int, int, None]) -> [int, ContentType]:
        """Read metadata (size, content type) of embedded data (in bytes) from generator

        Args:
            generator (generator): embedded data generator

        Returns:
            [int, ContentType]: embedded data size, content type 
        """
        size = self._get_integer(DATA_SIZE_BYTES, generator)
        contentType = ContentType(self._get_integer(MESSAGE_CONTENT_SIZE, generator))
            
        return size, contentType
    
    
    def _get_integer(self, numberOfBytes, generator: Generator[int, int, None]) -> int:
        """Get integer, that spans over `numberOfBytes`

        Args:
            numberOfBytes (int): number of bytes used to store the integer
            generator (Generator[int, int, None]): generates the bytes

        Returns:
            int: number stored in bytes
        """
        number = 0
        
        for i in range(numberOfBytes):
            byte = 0
            for j in range(self.BITS_IN_BYTES):
                bit = next(generator) << j
                byte += bit
            
            number += byte * 2**(self.BITS_IN_BYTES * (numberOfBytes - (i + 1)))
            
        return number