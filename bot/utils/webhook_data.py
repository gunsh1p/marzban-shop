import hashlib
import json
from base64 import b64encode

def check(data, key) -> bool:
    sign = data['sign']
    del data['sign']
    data = json.dumps(data, separators=(',', ':'))
    h = hashlib.md5((b64encode(data.encode('utf-8')).decode('utf-8') + key).encode('utf-8')).hexdigest()
    
    return sign == h