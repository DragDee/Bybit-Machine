import hashlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
import time

PUBLIC_KEY_PEM = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA6MIsf4XSrrbbOknUrtG9lBkaDB77agL6UzEwB/fUJVD/XFUvhF7LHIoBpfiDcgwlpBIAYL19oHqQ5H+pXqfAI3274rwbtOQt4IhqFre0pFKzT7alA0vJ1y/kXonPIaI4rq3oSSZkNg85eWL5Bc7JcbIyy70UrD12Kpv5LddFAEyRZdnDN7DqfoDndnWjSjwafDHzNYLiACvbWy+lcklXijwEYIPxmUvShqgs6cQAM6hBWTr7QwpNwc48U623PMAIrO6m22+v25YwoByKUWON4QaWReLR9spw781D0myiP50S0fX+sq0O4I3o6lDwHss50oE5uFhQ6JsR3LOzr0ZSuwIDAQAB
-----END PUBLIC KEY-----'''

def get_encrypted_pass_and_timestamp(password) -> tuple:

    password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
    timestamp = int(time.time() * 1000)
    input_string = f'{password_hash}:{timestamp}'
    public_key = RSA.import_key(PUBLIC_KEY_PEM)
    cipher = PKCS1_v1_5.new(public_key)
    encrypted_data = cipher.encrypt(input_string.encode('utf-8'))
    encoded_data = base64.b64encode(encrypted_data)

    return (encoded_data.decode('utf-8'), timestamp)


