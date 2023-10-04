import os

PARAMS = [
    'TOKEN'
]

def claim() -> list:
    config = []
    for param in PARAMS:
        value = os.environ.get(param)
        config.append(value)
    return value