from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `admin` ADD UNIQUE INDEX `uid_admin_usernam_6c25e3` (`username`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `admin` DROP INDEX `uid_admin_usernam_6c25e3`;"""
