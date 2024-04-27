from tortoise import Tortoise

from .config import load_config, config

load_config()

CONFIG_ORM = {
    "connections": {
        "mysql": {
            "engine": "tortoise.backends.asyncmy",
            "credentials": {
                "host": config.DB_HOST,
                "port": config.DB_PORT,
                "database": config.DB_NAME,
                "user": config.DB_USER,
                "password": config.DB_PASS,
            }
        }
    },
    "apps": {
        "default": {"models": ["db.models"], "default_connection": "mysql"}
    }
}

async def setup_db() -> None:
    await Tortoise.init(
        CONFIG_ORM
    )