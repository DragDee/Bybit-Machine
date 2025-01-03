import uuid
import time

def generate_login_name(email):
    string = email + str(time.time() * 1000)
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, string))
