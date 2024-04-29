from tortoise import Tortoise

from .config import config

CONFIG_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",
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
        "default": {
            "models": ["db.models", "aerich.models"], 
            "default_connection": "default"
        }
    }
}