import random


def encrypt_file(file, secret):
    print("file is being encrypted")
    initialization_vector = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])



