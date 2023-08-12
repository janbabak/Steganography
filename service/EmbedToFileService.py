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
            generator (AbstractGenerator): class responsible for generating data to embed
        
        Raises:
            RuntimeError
        """
        pass
        
        
    def embedBitIntoBite(self, byte, bit):
        """Embed bit into the leas significant bit of byte

        Args:
            byte (_type_): _description_
            bit (_type_): _description_

        Returns:
            _type_: _description_
        """
        return byte & bit
        # byteValue = int.from_bytes(byte, 'big')
        # return (byteValue - bit).to_bytes(1, 'big')
    