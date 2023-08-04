import random
import logging


class Encrypt:
    _instance = None
    _logger = logging.getLogger("service")

    @classmethod
    def get_instance(cls):
        """Create singleton instance

        Returns:
            Encrypt: singleton instance
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

    def encrypt_file(self, file, secret):
        """Encrypt file

        Args:
            file (string): path to the file being encrypted
            secret (string): secret key
        """
        self._logger.info("🙈 The file is being encrypted")
        init_vector = self._create_init_vector()
        self._logger.info(
            f"Init vector=\"{init_vector}\"")

    def _create_init_vector(self):
        """Create random initialization vector

        Returns:
            (string): 16 bytes init vector
        """
        return ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
