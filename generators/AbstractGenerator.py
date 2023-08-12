class AbstractGenerator:
    """Definition of Generator interface/abstract class
    """
    
    DATA_SIZE_BYTES = 4 # number of bytes used to store size info
    
    def generator(self) -> int:
        """Generates bits (starting from the leas significant bit), embeds the
        length of generated data (in bytes) before it

        Yields:
            int: bit
        """
        print('called')
    
    
    def get_size(self) -> int:
        """Get size of generated data in bytes
        
        Returns:
            int: number of bytes of data
        """
        pass