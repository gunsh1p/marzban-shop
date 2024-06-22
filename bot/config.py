import json
from dataclasses import dataclass, field

@dataclass
class Config:
    BOT_TOKEN: str = field(metadata={'json_name': 'BOT_TOKEN'})
    SECRET: str = field(metadata={'json_name': 'SECRET'})
    WEBHOOK_URL: str = field(metadata={'json_name': 'WEBHOOK_URL'})
    DEFAULT_LANG: str = field(metadata={'json_name': 'DEFAULT_LANG'})
    MAIN_ADMIN: int = field(metadata={'json_name': 'MAIN_ADMIN'})
    WEB_LOGIN: int = field(metadata={'json_name': 'WEB_LOGIN'})
    WEB_PASS: int = field(metadata={'json_name': 'WEB_PASS'})

def load_config() -> None:
    with open('config.json', 'rb') as file:
        json_data = json.load(file)
    return Config(**{k: json_data[v.metadata['json_name']] for k, v in Config.__dataclass_fields__.items() if v.metadata['json_name'] in json_data})

config: Config = load_config()