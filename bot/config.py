import json
from dataclasses import dataclass, field

@dataclass
class Config:
    BOT_TOKEN: str = field(init=False, metadata={'json_name': 'BOT_TOKEN'})
    BOT_SECRET: str = field(init=False, metadata={'json_name': 'BOT_SECRET'})
    MODE: str = field(init=False, metadata={'json_name': 'MODE'})
    MAIN_ADMIN: int = field(init=False, metadata={'json_name': 'MAIN_ADMIN'})

config: Config = None

def load_config() -> None:
    json_data = json.loads("config.json")
    config = Config(**{k: json_data[v['json_name']] for k, v in Config.__dataclass_fields__.items()})