# Marzban Shop

It is a Telegram bot shop powered by aiogram that provides VPN sales via Telegram

## Table of Contents

- [Features](#features)
- [Dependencies](#dependencies)
- [Installation guide](#installation-guide)
- [Configuration](#configuration)
- [To Do](#to-do)
- [Contributing](#contributing)
- [Donation](#donation)
- [License](#license)
- [Contacts](#contacts)

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

### Configuration

> You can set settings below using environment variables or placing them in `.env` file.

| Variable        | Description                                                                                                                                                        |
|-----------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| BOT_TOKEN       | Telegram bot token obtained from BotFather                                                                                                                         |
| SHOP_NAME       | Name of the VPN shop                                                                                                                                               |
| TEST_PERIOD     | Availability of test period (bool: true or false)                                                                                                                  |
| PERIOD_LIMIT    | Test period limit                                                                                                                                                  |
| ABOUT           | Service information                                                                                                                                                |
| RULES_LINK      | Link to service rules                                                                                                                                              |
| SUPPORT_LINK    | Link to service support                                                                                                                                            |
| YOOKASSA_TOKEN  | YooKassa's token                                                                                                                                                   |
| YOOKASSA_SHOPID | YooKassa's shopId                                                                                                                                                  |
| EMAIL           | Email for receipts                                                                                                                                                 |
| CRYPTO_TOKEN    | Cryptomus token                                                                                                                                                    |
| MERCHANT_UUID   | Cryptomus' Merchant UUID                                                                                                                                           |
| DB_NAME         | Database name                                                                                                                                                      |
| DB_USER         | Database username                                                                                                                                                  |
| DB_PASS         | Database password                                                                                                                                                  |
| DB_URL          | Url (like postgresql+psycopg://user:password@server/db) there user is DB_USER, password is DB_PASS, server is database IP (localhost by default) and db is DB_NAME |
| PANEL_HOST      | URL to connect to the marzban panel (if installed on the same server as marzban-shop, specify localhost and port of the panel)                                     |
| PANEL_GLOBAL    | URL to issue subscriptions (this parameter may be different from PANEL_HOST, more details [here](#difference-between-host-and-global))                             |
| PANEL_USER      | Panel username                                                                                                                                                     |
| PANEL_PASS      | Panel password                                                                                                                                                     |
| WEBHOOK_URL     | Webhook adress (url) (more deteails [here](#about-webhook))                                                                                                        |
| WEBHOOK_PORT    | Webhook port                                                                                                                                                       |

#### Difference between host and global

There are two environment variables PANEL_HOST and PANEL_GLOBAL

PANEL_HOST - address of the panel for interaction with API. If the panel is on the same server as marzban-shop, then localhost should be specified as the address. For example, <http://localhost:8080>

PANEL_GLOBAL - address for issuing subscriptions. It is used for substitution of a link to the subscription. It should be accessible not only in the local network, but also outside it

!WARNING! If the XRAY_SUBSCRIPTION_LINK variable in your marzban panel is set, leave the PANEL_GLOBAL variable empty

#### About webhook

To receive responses from the Telegram server and payment provider servers, webhook is used. This should be the address to which all these servers will contact. It must be a domain with TLS 1.2 or higher. Requests should be routed to the port you specified in .env in the WEBHOOK_PORT variable.
In addition, for YooKassa to work correctly, you will need to specify a webhook url in your personal account with the following value at the end of /yookassa_payment (e.g. <https://my-awesome-webhook.example.com/yookassa_payment>) and select all values that begin with payment

### To Do

- [ ] Storing items in db
- [ ] Web-panel for admins
- [ ] Code refactoring

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Donation

- BTC: `bc1qmrwu6uv00xcvsjvjkwnaw2ky6aenhjgqewg0w4`
- LTC: `ltc1qrl3fp7cwwxsun2fsk60zxgncuutkrydwgju6a2`
- USDT (TRC-20): `TJUUhJpeaZBBXpG6yUtzLsQmT3XQjViowV`
- ETH: `0x052D18812fA247Ce6853a6D95213CEbdb45c6277`

### License

The project is under the [GPL-3.0](https://github.com/gunsh1p/marzban-shop/blob/main/LICENSE) licence

### Contacts

Email: <bertollo@gunship.su>

Telegram: [@blackbloodredkiss](https://t.me/blackbloodredkiss)
