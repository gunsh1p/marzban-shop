import json

def get() -> list:
    with open("goods.json") as file:
        data = json.load(file)
    return data