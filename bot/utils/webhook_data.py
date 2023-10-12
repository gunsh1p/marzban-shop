import hashlib
import json
from base64 import b64encode

def check(data, key) -> bool:
    sign = data['sign']
    del data['sign']
    data = json.dumps(data)
    h = hashlib.md5(b64encode(data.encode('ascii')) + key.encode('ascii')).hexdigest()
    
    return sign == h