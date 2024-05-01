from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `tariff` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(64) NOT NULL,
    `description` LONGTEXT NOT NULL,
    `price` BIGINT NOT NULL,
    `period` INT NOT NULL,
    `panel_id` INT NOT NULL,
    CONSTRAINT `fk_tariff_panel_b36184a7` FOREIGN KEY (`panel_id`) REFERENCES `panel` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
        CREATE TABLE `tariff_inbound` (
    `inbound_id` INT NOT NULL REFERENCES `inbound` (`id`) ON DELETE CASCADE,
    `tariff_id` INT NOT NULL REFERENCES `tariff` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS `tariff_inbound`;
        DROP TABLE IF EXISTS `tariff`;"""
