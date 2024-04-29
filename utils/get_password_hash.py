import hashlib

def get_password_hash(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()