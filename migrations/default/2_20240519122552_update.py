from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `language` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(64) NOT NULL UNIQUE,
    `code` VARCHAR(5) NOT NULL UNIQUE
) CHARACTER SET utf8mb4;
        CREATE TABLE IF NOT EXISTS `scene` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(64) NOT NULL,
    `action` VARCHAR(64) NOT NULL,
    `text` LONGTEXT NOT NULL,
    `language_id` INT NOT NULL,
    CONSTRAINT `fk_scene_language_1f8e1b53` FOREIGN KEY (`language_id`) REFERENCES `language` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `language`;
        DROP TABLE IF EXISTS `scene`;"""
