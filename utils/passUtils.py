import binascii
import hashlib
import os
from typing import Any


def generateHash(word: Any):
    salt = hashlib.sha256(os.urandom(64)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', word.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (pwdhash + salt).decode('ascii')


def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    user_pass = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt,
                                  100000)
    pwdhash = binascii.hexlify(pwdhash)
    return pwdhash == user_pass
