import json
from dataclasses import dataclass, field

@dataclass
class DBConfig:
    DB_HOST: str = field(init=False, metadata={'json_name': 'DB_HOST'})
    DB_PORT: int = field(init=False, metadata={'json_name': 'DB_PORT'})
    DB_NAME: str = field(init=False, metadata={'json_name': 'DB_NAME'})
    DB_USER: str = field(init=False, metadata={'json_name': 'DB_USER'})
    DB_PASS: str = field(init=False, metadata={'json_name': 'DB_PASS'})

config: DBConfig = None

def load_config() -> None:
    json_data = json.loads("config.json")
    config = DBConfig(**{k: json_data[v['json_name']] for k, v in DBConfig.__dataclass_fields__.items()})