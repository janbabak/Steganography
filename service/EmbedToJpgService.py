import logging
from service.EmbedToFileService import EmbedToFileService

# jpg file structure: https://yasoob.me/posts/understanding-and-writing-jpeg-decoder-in-python/

class EmbedToJpgService(EmbedToFileService):
    """Embeds data to jpg/jpeg file.
    Singleton pattern
    """
    
    MARKER_LENGTH = 2
    SOS = 0xFFDA.to_bytes(MARKER_LENGTH, 'big') # Start Of Scan marker (after which row data starts)
    EOI = 0XFFD9.to_bytes(MARKER_LENGTH, 'big') # End Of Image marker
    
    
    _instance = None
    _log = logging.getLogger("EmbedToJpgService")
    
    
    @classmethod
    def get_instance(cls):
        """Create singleton instance

        Returns:
            EncryptService: singleton instance
        """
        if cls._instance == None:
            cls._instance = cls.__new__(cls)
        return cls._instance
    
    
    def embed_bytes(self, inputFilePath, outputFilePath, generator):
        """Embed bytes from generator to the input file

        Args:
            inputFilePath (string): path to the input file
            outputFilePath (string): path to the output file
            generator (AbstractGenerator): class responsible for generating data to embed

        Raises:
            RuntimeError: when input file header is corrupted
        """
        self._log.info("embed bytes to jpg")
        inputFile = self.process_header(inputFilePath, outputFilePath)
        
        if not inputFile:
            raise RuntimeError("Error while reading the header")
        
        outputFile = open(outputFilePath, "ab")
        previousByte = inputFile.read(1)
        currentByte = inputFile.read(1)
        
        while currentByte:
            # end of file
            if previousByte + currentByte == self.EOI:
                outputFile.write(self.EOI)
                outputFile.close()
                inputFile.close()
                self._log.info("end of file")
                return
            
            try:
                outputByte = self.createOutputByte(previousByte, next(generator.generator))
                print(outputByte)
                outputFile.write(outputByte)
            except:
                # there is no more bits to embed
                outputFile.write(previousByte)
                outputFile.write(currentByte)
                break
            
            previousByte = currentByte
            currentByte = inputFile.read(1)
            
        # copy the rest of the input file to the output file
        currentByte = inputFile.read(1)
        while currentByte:
            outputFile.write(currentByte)
            currentByte = inputFile.read(1)
            
            
        inputFile.close()
        outputFile.close()
            
        
        
    def process_header(self, inputFilePath, outputFilePath):
        """Read header of input file, save it into output file

        Args:
            inputFilePath (string): path to input file
            outputFilePath (string): path to input file

        Returns:
            File|False: input file descriptor ready to read image data, if success, False otherwise 
        """
        inputFile = open(inputFilePath, "rb")
        outputFile = open(outputFilePath, "wb")
        inputBytes = inputFile.read(1)
        outputFile.write(inputBytes)
        
        while inputBytes:
            inputBytes += inputFile.read(1)
            if inputBytes == self.SOS:
                outputFile.write(inputBytes[1:])
                outputFile.close()
                self._log.info("header processed")
                return inputFile
            inputBytes = inputBytes[1:]
            outputFile.write(inputBytes)
            
        inputFile.close()
        outputFile.close()
        
        self._log.error("🚨 Input file header is corrupted.")
            
        return False