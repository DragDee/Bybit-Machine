import json
import base64
import hashlib
import time

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Открытый ключ, предоставленный вами
PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAk4LV3DkKYiSTps5Jw/eb
cbSYVfqj9P7I97aZhHuxHR//w6CY7Cn4TMohVOVCm13MSLzxo0ugp/ceKhizz2BkS
vgHTji0hdwzfbSvj9C7chyxvRP9WrDRmW23fQU/bakzj/R+Rp5wLCeOCbTfVgZpz7
5DAdJcCmBZrjvYlvkuSPf3r+y4rnQ12dDwDMAix31IGiGtUMLZzxeAWMeRQPgo1lp
DIjwYM62/hhAhqV94oxIhTMKjgGMKbD6vHug325QD/KnStCbTE8qdGYkvAJUK89h3
Y5/LoGsNxct25dpzHsDZdBYhsrKUFHnqtxwH7fZFaBcLgzlnLCyOX5MknoAfNQIDA
QAB
-----END PUBLIC KEY-----"""

# XOR-ключ, предоставленный вами
XOR_KEY = "T9UHFQkNg7oQARdt"

def sort_keys(obj):
    if isinstance(obj, dict):
        return {k: sort_keys(obj[k]) for k in sorted(obj)}
    elif isinstance(obj, list):
        return [sort_keys(item) for item in obj]
    else:
        return obj

def convert_map_to_md5(data):
    sorted_data = sort_keys(data)
    json_str = json.dumps(sorted_data, separators=(',', ':'), ensure_ascii=False)
    md5_hash = hashlib.md5(json_str.encode('utf-8')).hexdigest()
    return md5_hash

def encrypt_with_public_key(message, public_key_pem):
    from cryptography.hazmat.backends import default_backend
    public_key = serialization.load_pem_public_key(
        public_key_pem.encode('utf-8'),
        backend=default_backend()
    )
    ciphertext = public_key.encrypt(
        message.encode('utf-8'),
        padding.PKCS1v15()
    )
    return ciphertext  # Возвращаем байты напрямую

def xor_bytes(data_bytes, key):
    key_bytes = key.encode('utf-8')
    key_length = len(key_bytes)
    xored = bytearray()
    for i in range(len(data_bytes)):
        xored.append(data_bytes[i] ^ key_bytes[i % key_length])
    return bytes(xored)

def encrypt_signature(api_endpoint, params_json_str):
    signature = ""
    try:
        version = "v1"
        md5_hash = ""
        if params_json_str:
            params = json.loads(params_json_str)
            md5_hash = convert_map_to_md5(params)
        timestamp = int(time.time() * 1000)
        timestamp_json = json.dumps({"timestamp": timestamp}, separators=(',', ':'))
        encoded_timestamp = base64.b64encode(timestamp_json.encode('utf-8')).decode('utf-8')

        data_to_encrypt = f"{api_endpoint}|{md5_hash}#timestamp:{timestamp}"
        print(f"Строка для шифрования: {data_to_encrypt}")

        encrypted_bytes = encrypt_with_public_key(data_to_encrypt, PUBLIC_KEY)
        xored_bytes = xor_bytes(encrypted_bytes, XOR_KEY)
        encoded_xored = base64.b64encode(xored_bytes).decode('utf-8')

        signature = f"{version}.{encoded_xored}.{encoded_timestamp}"

    except Exception as e:
        print("Ошибка при генерации подписи:", e)

    return signature

# Пример использования:
if __name__ == "__main__":
    # Замените на ваш API endpoint
    api_endpoint = "/api/endpoint"

    # Замените на вашу строку JSON параметров запроса
    params_json_str = '{"param1":"value1","param2":"value2"}'

    x_signature = encrypt_signature(api_endpoint, params_json_str)
    print("Сгенерированная x-signature:", x_signature)
