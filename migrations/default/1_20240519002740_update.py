from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` ADD `join_date` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6);
        ALTER TABLE `user` MODIFY COLUMN `balance` DOUBLE NOT NULL  DEFAULT 0;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `user` DROP COLUMN `join_date`;
        ALTER TABLE `user` MODIFY COLUMN `balance` BIGINT NOT NULL  DEFAULT 0;"""
