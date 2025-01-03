import hashlib

def encrypt_string(input_string):
    # Вычисляем SHA-256-хэш от MD5-хэша
    sha256_hash = hashlib.sha256(input_string.encode('utf-8')).hexdigest()
    return sha256_hash
