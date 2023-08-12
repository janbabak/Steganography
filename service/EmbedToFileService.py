class EmbedToFileService:
    """Embeds data to file.
    Abstract singleton
    """
    
    @classmethod
    def get_instance(cls):
        """Create singleton instance"""
        pass
    
    
    def embed_bytes(self, inputFilePath, outputFilePath, generator) -> None:
        """Embed bytes from generator to the input file

        Args:
            inputFilePath (string): path to the input file
            outputFilePath (string): path to the output file
            generator (generator): generates data to embed
        
        Raises:
            RuntimeError
        """
        pass
        
        
    def embed_bit_into_bite(self, byte, bit) -> bytes:
        """Embed bit into the leas significant bit of byte

        Args:
            byte (bytes): byte in which bit is embedded
            bit (int): bit embedded to bite

        Returns:
            bytes: byte with the least significant bite equal to bit
        """
        byte = (byte[0] >> 1) << 1 # make the least significant bit 0
        return (byte | bit).to_bytes(1, 'big') # 0 | 1 -> 1, 0 | 0 -> 0
    