import os

PARAMS = [
    'TOKEN',
    'NAME'
]

def claim() -> list:
    config = {}
    for param in PARAMS:
        value = os.environ.get(param)
        config[param] = value
    return config