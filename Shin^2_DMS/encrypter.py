"""
Proyecto Shin DMS
@author: Jose Pablo Castro
@author: David Jimenez
"""
from cryptography.fernet import Fernet
import os

f: str
files_list = [f for f in os.listdir() if os.path.isfile(f) and f != 'encrypter.py' and f != 'key.key']

def write_key():
    """
    Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    """
    Loads the key from the current directory named `key.key`
    """
    return open("key.key", "rb").read()

def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it encrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read all file data
        file_data = file.read()
        # encrypt data
        encrypted_data = f.encrypt(file_data)
        # write the encrypted file
        with open(filename, "wb") as file:
            file.write(encrypted_data)


def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    f = Fernet(key)
    with open(filename, "rb") as file:
        # read the encrypted data
        encrypted_data = file.read()
    # decrypt data
    decrypted_data = f.decrypt(encrypted_data)
    # write the original file
    with open(filename, "wb") as file:
        file.write(decrypted_data)

x = int(input("[1]Encriptar\n[2]Desencriptar\n[3]Generar Llave\n[4]Salir\n\nAccion:"))
if x == 3:
    write_key()
elif x == 1:
    for f in files_list:
        key = load_key()
        encrypt(f, key)
elif x == 2:
    for f in files_list:
        key = load_key()
        decrypt(f, key)