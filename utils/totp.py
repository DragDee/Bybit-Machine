import pyotp

def get_onetime_code_from_secret_totp(key: str):
    totp = pyotp.TOTP(key)
    current_otp = totp.now()

    return current_otp


if __name__ == '__main__':
    print(get_onetime_code_from_secret_totp(''))