import random
import logging
from Crypto.Cipher import AES
import os

class EncryptService:
    SECRET_LENGTH = 16
    INIT_VECTOR_LENGTH = 16
    
    _instance = None
    _log = logging.getLogger("EncryptService")


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
            secret (string): secret key, length must be 16 bytes, when shorter key used,
            pad by spaces, when longer is used, cut the remaining characters
        """
        self._log.info("🔐 The file is being encrypted")

        init_vector = self._create_init_vector()
        self._log.info(f"Init vector={init_vector}")
        
        data = self._get_file_content(file)
        secret = self._format_secret(secret)
        cipher = AES.new(secret, AES.MODE_CBC, init_vector)
        
        encrypted_data = cipher.encrypt(data)
        self._log.info(f"encrypted_data={encrypted_data}")
        return encrypted_data, init_vector
    
    
    def decrypt_file(self, file, secret, iv):
        self._log.info("🔓 The file is being decrypted")
        
        encrypted_data = file        
        secret = self._format_secret(secret)
        cipher = AES.new(secret, AES.MODE_CBC, iv)

        plain_text = cipher.decrypt(encrypted_data)
        self._log.info(f"plain text={plain_text}")
        return plain_text


    def _format_secret(self, secret):
        """Format secret key to SECRET_LENGTH and convert it into bytes, if longer, delete remaining bytes,
        if shorter, pad remaining bytes with spaces

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
        """Create random initialization vector of INIT_VECTOR_LENGTH length

        Returns:
            (bytes): init vector
        """
        return os.urandom(length)
    
    def _get_file_content(self, file):
        data = "Ahoj, jak se mas"
        return bytes(data, "utf-8")