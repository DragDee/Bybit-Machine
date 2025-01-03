import base64
import hashlib
import json
import time
from typing import Any
import asyncio

import requests
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding

PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAk4LV3DkKYiSTps5Jw/eb
cbSYVfqj9P7I97aZhHuxHR//w6CY7Cn4TMohVOVCm13MSLzxo0ugp/ceKhizz2BkS
vgHTji0hdwzfbSvj9C7chyxvRP9WrDRmW23fQU/bakzj/R+Rp5wLCeOCbTfVgZpz7
5DAdJcCmBZrjvYlvkuSPf3r+y4rnQ12dDwDMAix31IGiGtUMLZzxeAWMeRQPgo1lp
DIjwYM62/hhAhqV94oxIhTMKjgGMKbD6vHug325QD/KnStCbTE8qdGYkvAJUK89h3
Y5/LoGsNxct25dpzHsDZdBYhsrKUFHnqtxwH7fZFaBcLgzlnLCyOX5MknoAfNQIDA
QAB
-----END PUBLIC KEY-----"""

XOR_KEY = "T9UHFQkNg7oQARdt"


def buffer_to_hex(encrypted_bytes: bytes, key_size: int) -> str:
    hex_str = encrypted_bytes.hex().upper()
    expected_length = key_size * 2
    return hex_str.zfill(expected_length)


def sort_object_keys_recursive(obj: Any) -> Any:
    if isinstance(obj, list):
        return [sort_object_keys_recursive(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: sort_object_keys_recursive(obj[key]) for key in sorted(obj)}
    else:
        return obj


def generate_md5_hash(data: Any) -> str:
    sorted_data = json.dumps(sort_object_keys_recursive(data), separators=(",", ":"))

    md5_hash = hashlib.md5()
    md5_hash.update(sorted_data.encode("utf-8"))
    return md5_hash.hexdigest()


def xor_strings(data: str, key: str) -> str:
    result = []
    key_length = len(key)
    for i, char in enumerate(data):
        xor_char = chr(ord(char) ^ ord(key[i % key_length]))
        result.append(xor_char)
    return "".join(result)


def encrypt_with_public_key(data: str, public_key_pem: str, key_size: int = 1024) -> str:
    try:
        public_key = serialization.load_pem_public_key(public_key_pem.encode("utf-8"), backend=default_backend())

        encrypted = public_key.encrypt(data.encode("utf-8"), padding.PKCS1v15())

        encrypted_hex = buffer_to_hex(encrypted, key_size)

        return encrypted_hex
    except Exception as e:
        print("Ошибка при шифровании:", e)
        return None


def generate_signature(base_string: str, json_data: str) -> str:
    version = "v1"
    signature = ""

    try:
        if json_data:
            parsed_data = json.loads(json_data)
            hash_value = generate_md5_hash(parsed_data)
        else:
            hash_value = ""
        timestamp = int(time.time() * 1000)

        timestamp_json = json.dumps({"timestamp": timestamp}, separators=(",", ":"))
        encoded_timestamp = base64.b64encode(timestamp_json.encode("utf-8")).decode("utf-8")

        data_to_encrypt = f"{base_string}|{hash_value}#timestamp:{timestamp}"

        encrypted_hex = encrypt_with_public_key(data_to_encrypt, PUBLIC_KEY)
        if not encrypted_hex:
            raise Exception("Encryption failed")

        xored = xor_strings(encrypted_hex, XOR_KEY)
        encoded_xored = base64.b64encode(xored.encode("utf-8")).decode("utf-8")

        signature = f"{version}.{encoded_xored}.{encoded_timestamp}"

    except Exception as e:
        print("Error generating token:", e)


    return signature


async def main():
    # тут заполни
    risk_token = ""
    email_verify = ""
    google2fa = ""

    base_string = ""
    json_data = {
        "risk_token": risk_token,
        "component_list": {
            "email_verify": email_verify,
            "google2fa": google2fa,
        },
    }

    signature = await generate_signature(base_string, json.dumps(json_data))

    # тут заполни куки
    cookies = {}


    headers = {
            "accept": "application/json",
            "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/json;charset=UTF-8",
            "gdfp": "dmVyMQ|MTNhZjg2Zjc1ZG0wem45aDJwd2pveTk2MTU5OTA4NDhl||v2:gRoG/yXpWm2/MGeG63YEkdYLXEQ4EtNeZfW8rLR0FZ5u6BqQCXuwtbyRy0n5ir4lL65xxddgNKP1YSdTpJtv2HJ+065T06PvrypRh7p+B9BmlfpR7aRY1dtIJcXyzoEaEcdXZUszmfRiNvXO3dLt+77canvB/Bb3sY/m0kHtNo9VKIUs5Hp/r3XJT8spo1qXof7l543jGbauupcOF/85lynby6Axj3wDMhK+YOCrbnjQ8lXmK8bb",
            "guid": "9fc624d9-32ae-2e30-65d7-557ed76d813e",
            "lang": "en",
            "origin": "https://www.bybit.com",
            "platform": "pc",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://www.bybit.com/",
            "sec-ch-ua": '"Not)A;Brand";v="99", "Opera GX";v="113", "Chromium";v="127"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "traceparent": "00-d170fedadc574f43f8c9d906e8287706-013d78b8fe41b5ae-01",
            "tx-id": "dmVyMQ|MTNhZjg2Zjc1ZG0wem45aDJwd2pveTk2MTU5OTA4NDhl||v2:gRoG/yXpWm2/MGeG63YEkdYLXEQ4EtNeZfW8rLR0FZ5u6BqQCXuwtbyRy0n5ir4lL65xxddgNKP1YSdTpJtv2HJ+065T06PvrypRh7p+B9BmlfpR7aRY1dtIJcXyzoEaEcdXZUszmfRiNvXO3dLt+77canvB/Bb3sY/m0kHtNo9VKIUs5Hp/r3XJT8spo1qXof7l543jGbauupcOF/85lynby6Axj3wDMhK+YOCrbnjQ8lXmK8bb",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0 (Edition Yx GX)",
            "x-signature": signature,
        }

    response = requests.post(
        "https://api2.bybit.com/user/public/risk/verify", cookies=cookies, headers=headers, json=json_data
    )

    response_data = response.json()

    print(response.status_code)

    print(response_data)


if __name__ == '__main__':


    asyncio.run(main())
