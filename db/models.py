from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    tid = fields.BigIntField()
    username = fields.CharField(max_length=32)
    email = fields.CharField(max_length=256)
    lang = fields.CharField(max_length=5, default="none")
    status = fields.CharField(max_length=10, default="active")
    balance = fields.BigIntField(default=0)

    def __str__(self) -> str:
        return f"{self.id}. {self.username} - {self.lang} (user)"

class Referral(Model):
    id = fields.IntField(pk=True)
    owner = fields.OneToOneField('default.User', related_name='referrers_owner')
    referrer = fields.OneToOneField('default.User', related_name='referrer')

    def __str__(self):
        return f'{self.id}. {self.referrer.username} (referrer)'

class TestSubscription(Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField('default.User')

    def __str__(self) -> str:
        return f"Test subscription {self.id}"

class Admin(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=64, unique=True)
    password = fields.CharField(max_length=32)
    
    def __str__(self) -> str:
        return f'{self.id}. {self.username} (admin)'