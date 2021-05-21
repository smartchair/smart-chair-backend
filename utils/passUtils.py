import binascii
import hashlib
import os
from typing import Any


def generateHash(word: Any):
    salt = hashlib.sha256(os.urandom(64)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', word.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return {'salt': salt, 'key': pwdhash}


def verify_password(stored_password, provided_password):
    salt = stored_password['salt']
    key = stored_password['key']
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt,
                                  100000)
    pwdhash = binascii.hexlify(pwdhash)
    if str(pwdhash) == key:
        print("pwdhash "+ str(pwdhash))
        print("KEY " + key)
        print("verify TRUE")
        return True
    else:
        print("verify FALSE")
        return False
