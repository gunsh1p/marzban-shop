import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tortoise import Tortoise

from db.setup import CONFIG_ORM
from routers import auth
from middlewares.check_auth import CheckAuthMiddleware


async def setup_db():
    await Tortoise.init(
        CONFIG_ORM
    )

def setup_middlewares(app: FastAPI):
    app.middleware('http')(CheckAuthMiddleware())
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
def setup_routers(app: FastAPI):
    auth.register_router(app)

def get_app() -> FastAPI:
    app = FastAPI()
    asyncio.gather(setup_db())
    setup_middlewares(app)
    setup_routers(app)
    
    return app