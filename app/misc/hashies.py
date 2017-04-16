import hashlib
import shortid


def md5(string):
    return hashlib.md5(string).hexdigest()


def short_id():
    return shortid.ShortId().generate()
