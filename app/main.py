import asyncio

from fastapi import FastAPI
from tortoise import Tortoise

from db.setup import CONFIG_ORM
from routers import (
    auth,
    statistics,
    languages
)
from middlewares.check_auth import CheckAuthMiddleware


async def setup_db():
    await Tortoise.init(
        CONFIG_ORM
    )

def setup_middlewares(app: FastAPI):
    app.middleware('http')(CheckAuthMiddleware())
    
def setup_routers(app: FastAPI):
    auth.register_router(app)
    statistics.register_router(app)
    languages.register_router(app)

def get_app() -> FastAPI:
    app = FastAPI()
    asyncio.gather(setup_db())
    setup_middlewares(app)
    setup_routers(app)
    
    return app