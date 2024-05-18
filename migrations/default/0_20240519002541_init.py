from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `admin` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(64) NOT NULL UNIQUE,
    `password` VARCHAR(32) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `panel` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(64) NOT NULL,
    `username` VARCHAR(64) NOT NULL,
    `password` VARCHAR(64) NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `inbound` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(64) NOT NULL,
    `panel_id` INT NOT NULL,
    CONSTRAINT `fk_inbound_panel_97e3e097` FOREIGN KEY (`panel_id`) REFERENCES `panel` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `tariff` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `title` VARCHAR(64) NOT NULL,
    `description` LONGTEXT NOT NULL,
    `price` BIGINT NOT NULL,
    `period` INT NOT NULL,
    `panel_id` INT NOT NULL,
    CONSTRAINT `fk_tariff_panel_b36184a7` FOREIGN KEY (`panel_id`) REFERENCES `panel` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `tid` BIGINT NOT NULL,
    `username` VARCHAR(32) NOT NULL,
    `email` VARCHAR(256) NOT NULL,
    `lang` VARCHAR(5) NOT NULL  DEFAULT 'none',
    `status` VARCHAR(10) NOT NULL  DEFAULT 'active',
    `balance` BIGINT NOT NULL  DEFAULT 0
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `buy` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `tariff_id` INT,
    `user_id` INT,
    CONSTRAINT `fk_buy_tariff_28a02e8d` FOREIGN KEY (`tariff_id`) REFERENCES `tariff` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_buy_user_8c51698b` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `online` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `time` DATETIME(6) NOT NULL  DEFAULT CURRENT_TIMESTAMP(6),
    `user_id` INT NOT NULL,
    CONSTRAINT `fk_online_user_2b57d0b2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `referral` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `owner_id` INT NOT NULL UNIQUE,
    `referrer_id` INT NOT NULL UNIQUE,
    CONSTRAINT `fk_referral_user_cc19ac9f` FOREIGN KEY (`owner_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_referral_user_0a7b6dcf` FOREIGN KEY (`referrer_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `testsubscription` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `user_id` INT NOT NULL UNIQUE,
    CONSTRAINT `fk_testsubs_user_6297e2c2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `tariff_inbound` (
    `tariff_id` INT NOT NULL,
    `inbound_id` INT NOT NULL,
    FOREIGN KEY (`tariff_id`) REFERENCES `tariff` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`inbound_id`) REFERENCES `inbound` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
