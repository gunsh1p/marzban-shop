from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    tid = fields.BigIntField()
    username = fields.CharField(max_length=32)
    email = fields.CharField(max_length=256)
    lang = fields.CharField(max_length=5, default="none")
    status = fields.CharField(max_length=10, default="active")
    balance = fields.FloatField(default=0)
    join_date = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.id}. {self.username} - {self.lang} (user)"

    def to_dict(self) -> dict:
        join_date = self.join_date.strftime("%d-%m-%Y")
        content = {
            "id": self.id,
            "telegram_id": self.tid,
            "username": self.username,
            "email": self.email,
            "language": self.lang,
            "status": self.status,
            "balance": round(self.balance, 2),
            "time": join_date,
        }
        return content


class Online(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("default.User", null=True, on_delete=fields.NO_ACTION)
    time = fields.DatetimeField(auto_now_add=True)

    async def to_dict(self) -> dict:
        user = await self.user
        date = self.time.strftime("%d-%m-%Y")
        content = {"id": user, "user": self.user, "time": date}
        return content


class Referral(Model):
    id = fields.IntField(pk=True)
    owner = fields.OneToOneField("default.User", related_name="referrers_owner")
    referrer = fields.OneToOneField("default.User", related_name="referrer")

    def __str__(self):
        return f"{self.id}. {self.referrer.tid} (referrer)"


class TestSubscription(Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField("default.User")

    def __str__(self) -> str:
        return f"Test subscription {self.id}"


class Panel(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=64)
    username = fields.CharField(max_length=64)
    password = fields.CharField(max_length=64)


class Inbound(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=64)
    panel = fields.ForeignKeyField("default.Panel")


class Tariff(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=64)
    description = fields.TextField()
    price = fields.BigIntField()
    period = fields.IntField()
    panel = fields.ForeignKeyField("default.Panel")
    inbounds = fields.ManyToManyField("default.Inbound", on_delete=fields.CASCADE)


class Buy(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("default.User", on_delete=fields.CASCADE, null=True)
    tariff = fields.ForeignKeyField(
        "default.Tariff", on_delete=fields.CASCADE, null=True
    )
    time = fields.DatetimeField(auto_now_add=True)

    async def to_dict(self) -> dict:
        user: User | None = await self.user
        tariff: Tariff | None = await self.tariff
        date = self.time.strftime("%d-%m-%Y")
        content = {"id": self.id, "user": user, "tariff": tariff, "time": date}
        return content


class Admin(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=64, unique=True)
    password = fields.CharField(max_length=32)

    def __str__(self) -> str:
        return f"{self.id}. {self.username} (admin)"


class Language(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=64, unique=True)
    code = fields.CharField(max_length=5, unique=True)

    def __str__(self) -> str:
        return f"{self.id}. {self.title} ({self.code})"

    def to_dict(self) -> dict:
        content = {"id": self.id, "title": self.title, "code": self.code}
        return content


class Scene(Model):
    id = fields.IntField(pk=True)
    language = fields.ForeignKeyField("default.Language")
    title = fields.CharField(max_length=64)
    action = fields.CharField(max_length=64)
    text = fields.TextField()

    async def to_dict(self) -> dict:
        lang: Language = await self.language
        content = {
            "id": self.id,
            "language": lang.code,
            "title": self.title,
            "action": self.action,
            "text": self.text,
        }
        return content