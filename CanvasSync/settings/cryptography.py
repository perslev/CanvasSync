"""
CanvasSync by Mathias Perslev
February 2017

--------------------------------------------

cryptography.py, module

Functions used to encrypt and decrypt the settings stored in the .CanvasSync.settings file. When the user has specified
settings the string of information is encrypted using the AES 256 module of the PyCrypto library. A password is
specified by the user upon creation of the settings file. A hashed (thus unreadable) version of the password is stored
locally in the .ps.sync file in the home folder of the user. Upon launch of CanvasSync, the user must specify
a password that matches the one stored in the hashed version. If the password is correct the the settings file is
decrypted and parsed for settings.
"""

# Future imports
from __future__ import print_function

# Inbuilt modules
import getpass
import os.path
import sys

# Third party modules
import bcrypt
from Crypto.Cipher import AES
from Crypto.Hash import SHA256


def get_key_hash(password):
    """ Get a 256 byte SHA hash from any length password """
    hasher = SHA256.new(password.encode(u"utf-8"))
    return hasher.digest()


def encrypt(message):
    """
    Encrypts a string using AES-256 (CBC) encryption
    A random initialization vector (IV) is padded as the initial 16 bytes of the string
    The encrypted message will be padded to length%16 = 0 bytes (AES needs 16 bytes block sizes)
    """

    print(u"\nPlease enter a password to encrypt the settings file:")
    hashed_password = bcrypt.hashpw(getpass.getpass(), bcrypt.gensalt())
    with open(os.path.expanduser(u"~") + u"/.CanvasSync.pw", "w") as pass_file:
        pass_file.write(hashed_password)

    # Generate random 16 bytes IV
    IV = os.urandom(16)

    # AES object
    encrypter = AES.new(get_key_hash(hashed_password), AES.MODE_CBC, IV)

    # Padding to 16 bytes
    if len(message) % 16 != 0:
        message += " " * (16 - (len(message) % 16))

    # Add the unencrypted IV to the beginning of the encrypted_message
    encrypted_message = IV + encrypter.encrypt(message.encode("utf-8"))

    return encrypted_message


def decrypt(message, password):
    """
    Decrypts an AES encrypted string
    """

    # Load the locally stored bcrypt hashed password (answer)
    path = os.path.expanduser(u"~") + u"/.CanvasSync.pw"
    if not os.path.exists(path):
        return False

    with open(path, "r") as pw_file:
        hashed_password = pw_file.read()

    # Get password from user and compare to answer
    valid_password = False

    # If the password isn't null then it was specified as a command-line argument
    if password:
        if bcrypt.hashpw(password, hashed_password) != hashed_password:
            print(u"\n[ERROR] Invalid password. Please try again or invoke CanvasSync with the -s flag to reset settings.")
            sys.exit()
    else:
        # Otherwise, get the password from the user
        while not valid_password:
            print(u"\nPlease enter password to decrypt the settings file:")
            password = getpass.getpass()
            if bcrypt.hashpw(password, hashed_password) == hashed_password:
                valid_password = True
            else:
                print(u"\n[ERROR] Invalid password. Please try again or invoke CanvasSync with the -s flag to reset settings.")

    # Read the remote IV
    remoteIV = message[:16]

    # Decrypt message using the correct password
    decrypter = AES.new(get_key_hash(hashed_password), AES.MODE_CBC, remoteIV)
    decrypted_message = decrypter.decrypt(message[16:])

    return decrypted_message.rstrip()
