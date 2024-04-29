import json
from dataclasses import dataclass, field

@dataclass
class DBConfig:
    DB_HOST: str = field(metadata={'json_name': 'DB_HOST'})
    DB_PORT: int = field(metadata={'json_name': 'DB_PORT'})
    DB_NAME: str = field(metadata={'json_name': 'DB_NAME'})
    DB_USER: str = field(metadata={'json_name': 'DB_USER'})
    DB_PASS: str = field(metadata={'json_name': 'DB_PASS'})

def load_config() -> DBConfig:
    with open('config.json', 'rb') as file:
        json_data = json.load(file)
    return DBConfig(**{k: json_data[v.metadata['json_name']] for k, v in DBConfig.__dataclass_fields__.items() if v.metadata['json_name'] in json_data})

config: DBConfig = load_config()