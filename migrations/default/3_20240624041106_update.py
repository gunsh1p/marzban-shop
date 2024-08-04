from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `buy` MODIFY COLUMN `tariff_id` INT;
        ALTER TABLE `buy` MODIFY COLUMN `user_id` INT;
        ALTER TABLE `inbound` MODIFY COLUMN `panel_id` INT NOT NULL;
        ALTER TABLE `online` MODIFY COLUMN `user_id` INT;
        ALTER TABLE `online` MODIFY COLUMN `user_id` INT;
        ALTER TABLE `referral` MODIFY COLUMN `owner_id` INT NOT NULL;
        ALTER TABLE `referral` MODIFY COLUMN `referrer_id` INT NOT NULL;
        ALTER TABLE `scene` MODIFY COLUMN `language_id` INT NOT NULL;
        ALTER TABLE `tariff` MODIFY COLUMN `panel_id` INT NOT NULL;
        ALTER TABLE `testsubscription` MODIFY COLUMN `user_id` INT NOT NULL;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `buy` MODIFY COLUMN `tariff_id` INT;
        ALTER TABLE `buy` MODIFY COLUMN `user_id` INT;
        ALTER TABLE `inbound` MODIFY COLUMN `panel_id` INT NOT NULL;
        ALTER TABLE `online` MODIFY COLUMN `user_id` INT NOT NULL;
        ALTER TABLE `online` MODIFY COLUMN `user_id` INT NOT NULL;
        ALTER TABLE `referral` MODIFY COLUMN `owner_id` INT NOT NULL;
        ALTER TABLE `referral` MODIFY COLUMN `referrer_id` INT NOT NULL;
        ALTER TABLE `scene` MODIFY COLUMN `language_id` INT NOT NULL;
        ALTER TABLE `tariff` MODIFY COLUMN `panel_id` INT NOT NULL;
        ALTER TABLE `testsubscription` MODIFY COLUMN `user_id` INT NOT NULL;"""
