from tortoise.models import Model
from tortoise import fields

class User(Model):
    id = fields.IntField(pk=True)
    tid = fields.BigIntField()
    username = fields.CharField(max_length=64)
    photo_id = fields.CharField(max_length=100)
    lang = fields.CharField(max_length=5, default="none")
    status = fields.CharField(max_length=10, default="active")
    balance = fields.BigIntField(default=0)

    def __str__(self):
        return f"{self.id}. {self.username} - {self.lang}"

class Referral(Model):
    id = fields.IntField(pk=True)
    owner = fields.OneToOneField('default.User', related_name='referral_owner')
    referrer = fields.OneToOneField('default.User', related_name='referrer')

    def __str__(self):
        return f'Referrer - {self.id}'

class TestSubscription(Model):
    id = fields.IntField(pk=True)
    user = fields.OneToOneField('default.User')

    def __str__(self):
        return "Test subscription " + str(self.user)