# Marzban Shop

It is a Telegram bot shop powered by aiogram that provides VPN sales via Telegram

## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installation guide](#installation-guide)
- [Configuration](#configuration)
- [To Do](#to-do)
- [Donation](#donation)
- [License](#license)
- [Contributors](#contributors)

### Features

- Test subscriptions
- Two payment methods: [Cryptomus](https://cryptomus.com/) and [YooKassa](https://yookassa.ru/)
- Interface in Russian and English

### Dependencies

- [Docker](https://www.docker.com/)

### Installation guide

#### Setup

```bash
git clone https://github.com/gunsh1p/marzban-shop.git
cd marzban-shop
docker compose build
```

After that edit goods.examples.json

##### Good example

```json
{
        "title": <your_title_here>,
        "price": {
            "en": <price_for_crypto_payments>,
            "ru": <price_for_yookassa_payments>
        },
        "callback": <unique_id_for_good>,
        "months": <umber_of_months>
    }
```

And edit .env.example file (see [configuration](#configuration))

After all run this code

```bash
mv goods.example.json goods.json
mv .env.example .env
```

#### Run

```bash
docker compose up -d
```

## Configuration

> You can set settings below using environment variables or placing them in `.env` file.

| Variable        | Description                                                                                                                                 |
|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------|
| BOT_TOKEN       | Telegram bot token obtained from BotFather                                                                                                  |
| SHOP_NAME       | Name of the VPN shop                                                                                                                        |
| TEST_PERIOD     | Availability of test period (bool: true or false)                                                                                           |
| PERIOD_LIMIT    | Test period limit                                                                                                                           |
| ABOUT           | Service information                                                                                                                         |
| RULES_LINK      | Link to service rules                                                                                                                       |
| SUPPORT_LINK    | Link to service support                                                                                                                     |
| YOOKASSA_TOKEN  | YooKassa's token                                                                                                                            |
| YOOKASSA_SHOPID | YooKassa's shopId                                                                                                                           |
| CRYPTO_TOKEN    | Cryptomus token                                                                                                                             |
| MERCHANT_UUID   | Cryptomus' Merchant UUID                                                                                                                    |
| DB_NAME         | Database name                                                                                                                               |
| DB_USER         | Database username                                                                                                                           |
| DB_PASS         | Database password                                                                                                                           |
| DB_URL          | Url (like postgresql+psycopg://user:password@server/db) there user is DB_USER, password, server is database IP is DB_PASS and db is DB_NAME |
| PANEL_HOST      | URL to connect to the marzban panel (if installed on the same server as marzban-shop, specify localhost and port of the panel)              |
| PANEL_GLOBAL    | URL to issue subscriptions (this parameter may be different from PANEL_HOST, more details [here](#difference-between-host-and-global))                                             |
| PANEL_USER      | Panel username                                                                                                                              |
| PANEL_PASS      | Panel password                                                                                                                              |
| WEBHOOK_URL     | Webhook adress (url) (more deteails [here](#about-webhook))                                                                                                   |
| WEBHOOK_PORT    | Webhook port                                                                                                                                |

### Difference between host and global

There are two environment variables PANEL_HOST and PANEL_GLOBAL
PANEL_HOST - address of the panel for interaction with API. If the panel is on the same server as marzban-shop, then localhost should be specified as the address. For example, <http://localhost:8080>
PANEL_GLOBAL - address for issuing subscriptions. It is used for substitution of a link to the subscription. It should be accessible not only in the local network, but also outside it

### About webhook
