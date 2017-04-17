import hashlib
import shortid


def md5(string):
    return hashlib.md5(string).hexdigest()


def short_id():
    return shortid.ShortId().generate()


def sign_string(string, salt):
    key = '{}-{}'.format(string, salt)
    return hashlib.sha256(key).hexdigest()


def validate_string_signature(string, salt, signature):
    return sign_string(string, salt) == signature
