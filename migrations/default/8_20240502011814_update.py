from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `buy` MODIFY COLUMN `tariff_id` INT;
        ALTER TABLE `buy` MODIFY COLUMN `user_id` INT;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `buy` MODIFY COLUMN `tariff_id` INT NOT NULL;
        ALTER TABLE `buy` MODIFY COLUMN `user_id` INT NOT NULL;"""
