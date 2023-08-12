import os
import logging
from Crypto.Cipher import AES

class EncryptService:
    """Responsible for encrypting and decryption files using AES cipher.
    Singleton pattern.
    """
    
    SECRET_LENGTH = 16
    INIT_VECTOR_LENGTH = 16
    FILE_SIZE_LENGTH = 4 # number of bytes used for storing original file size
    CHUNK_SIZE = 16 # number of bytes being encrypted or decrypted
    
    _instance = None
    _log = logging.getLogger("EncryptService")


    @classmethod
    def get_instance(cls):
        """Create singleton instance

        Returns:
            EncryptService: singleton instance
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
    

    def encrypt_file(self, inputFilePath, outputFilePath, secret, blockMode=AES.MODE_CBC):
        """Encrypt file chunk by chunk

        Args:
            inputFilePath (string): path to the input file
            outputFilePath (string): path to the output file
            secret (string): secret key used for encryption and decryption
            blockMode (number, optional): Block cipher mode. Defaults to AES.MODE_CBC.
        """
        secret = self._format_secret(secret)
        initVector = self._create_init_vector()
        self._log.info(f"Init vector={initVector}")
        
        cipher = AES.new(secret, blockMode, initVector)
        
        self.save_header(inputFilePath, outputFilePath, initVector)
        
        inputFile = open(inputFilePath, "rb")
        outputFile = open(outputFilePath, "ab")
        inputBytes = True

        while inputBytes:
            inputBytes = inputFile.read(self.CHUNK_SIZE)
            
            if not inputBytes:
                break
            
            # if input bytes aren't aligned to CHUNK_SIZE, add padding of spaces
            if len(inputBytes) < self.CHUNK_SIZE:
                paddingLength = self.CHUNK_SIZE - len(inputBytes)
                inputBytes += bytes(" " * paddingLength, "utf-8")
                
            outputBytes = cipher.encrypt(inputBytes)
            outputFile.write(outputBytes)
            
        inputFile.close()
        outputFile.close()
        
        self._log.info(f"🔐 File \"{inputFilePath}\" was encrypted.")
        
    
    def decrypt_file(self, inputFilePath, outputFilePath, secret, blockMode=AES.MODE_CBC):
        """Decrypt file chunk by chunk

        Args:
            inputFilePath (string): path to the input file
            outputFilePath (string): path to the output file
            secret (string): secret key used for encryption and decryption
            blockMode (number, optional): Block cipher mode.. Defaults to AES.MODE_CBC.
        """
               
        numberOfBytesToRead, initVector, inputFile = self.read_header(inputFilePath)

        secret = self._format_secret(secret)
        cipher = AES.new(secret, blockMode, initVector)
        outputFile = open(outputFilePath, "wb")
        inputBytes = True

        while inputBytes:
            inputBytes = inputFile.read(self.CHUNK_SIZE)
            numberOfBytesToRead -= len(inputBytes)
            
            if not inputBytes:
                break
                
            outputBytes = cipher.decrypt(inputBytes)
            
            # if last chunk
            if numberOfBytesToRead <= self.CHUNK_SIZE:
                outputBytes = outputBytes[0 : numberOfBytesToRead]
            
            outputFile.write(outputBytes)
            
        inputFile.close()
        outputFile.close()
            
        self._log.info(f"🔓 File {inputFilePath} was decrypted")

            
    def save_header(self, inputFilePath, outputFilePath, initVector):
        """Save header containing metadata (file size, init vector) to output file

        Args:
            inputFilePath (string): path to the input file
            outputFilePath (string): path to the output file
            initVector (bytes): init vector
        """
        outputFile = open(outputFilePath, "wb")
        inputFileSize = os.path.getsize(inputFilePath)
        outputFile.write(inputFileSize.to_bytes(self.FILE_SIZE_LENGTH, "big"))
        outputFile.write(initVector)
        
        self._log.info(f"👦 Saved header - fileSize={inputFileSize}, initVector={initVector}")
        
        
    def read_header(self, inputFilePath):
        """Read header of encrypted file containing decrypted file size and init vector

        Args:
            inputFilePath (string): path to the input file

        Returns:
            (number, bytes, file): file size, init vector, input file descriptor
        """
        inputFile = open(inputFilePath, "rb")
        fileSize = int.from_bytes(inputFile.read(self.FILE_SIZE_LENGTH), 'big')
        initVector = inputFile.read(self.INIT_VECTOR_LENGTH)
        
        self._log.info(f"👦 Read header - fileSize={fileSize}, initVector={initVector}")

        return fileSize, initVector, inputFile


    def _format_secret(self, secret):
        """Format secret key to SECRET_LENGTH and convert it into bytes, if longer, delete remaining
        bytes, if shorter, pad remaining bytes with spaces

        Args:
            secret (string): secret key

        Returns:
            bytes: formatted secret
        """
        if len(secret) < self.SECRET_LENGTH:
            secret = secret + ' ' * (self.SECRET_LENGTH - len(secret))
        elif len(secret) > self.SECRET_LENGTH:
            secret = secret[0: self.SECRET_LENGTH]
        return bytes(secret, 'utf-8')


    def _create_init_vector(self, length=INIT_VECTOR_LENGTH):
        """Create random initialization vector of chosen length

        Returns:
            (bytes): init vector
        """
        return os.urandom(length)