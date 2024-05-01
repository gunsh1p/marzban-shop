from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `buy` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `tariff_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_buy_tariff_28a02e8d` FOREIGN KEY (`tariff_id`) REFERENCES `tariff` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_buy_user_8c51698b` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `buy`;"""
