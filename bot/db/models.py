from sqlalchemy import Column, BigInteger, String, Boolean

from db.base import Base

class VPNUsers(Base):
    __tablename__ = "vpnusers"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    tg_id = Column(BigInteger)
    vpn_id = Column(String(64), default="")
    test = Column(Boolean, default=False)

class CPayments(Base):
    __tablename__ = "crypto_payments"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    tg_id = Column(BigInteger)
    lang = Column(String(64))
    payment_uuid = Column(String(64))
    order_id = Column(String(64))
    chat_id = Column(BigInteger)
    callback = Column(String(64))

class YPayments(Base):
    __tablename__ = "yookassa_payments"

    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    tg_id = Column(BigInteger)
    lang = Column(String(64))
    payment_id = Column(String(64))
    chat_id = Column(BigInteger)
    callback = Column(String(64))