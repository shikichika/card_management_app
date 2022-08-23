import hashlib

def hash (name, password):

    #merge name and password
    merge_word = (name + password).encode("utf-8")

    #hash
    hash_password = hashlib.md5(merge_word).hexdigest()

    return hash_password


