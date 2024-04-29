from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `admin` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `username` VARCHAR(64) NOT NULL,
    `password` VARCHAR(32) NOT NULL
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
CREATE TABLE IF NOT EXISTS `referral` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `referrer_id` INT NOT NULL UNIQUE,
    `owner_id` INT NOT NULL UNIQUE,
    CONSTRAINT `fk_referral_user_0a7b6dcf` FOREIGN KEY (`referrer_id`) REFERENCES `user` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_referral_user_cc19ac9f` FOREIGN KEY (`owner_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
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
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
