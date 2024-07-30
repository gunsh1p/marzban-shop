import hashlib

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import insert, select, update, delete

from db.models import YPayments, CPayments, VPNUsers
import glv

engine = create_async_engine(glv.config['DB_URL'])

async def create_vpn_profile(tg_id: int):
    async with engine.connect() as conn:
        sql_query = select(VPNUsers).where(VPNUsers.tg_id == tg_id)
        result: VPNUsers = (await conn.execute(sql_query)).fetchone()
        if result != None:
            return
        hash = hashlib.md5(str(tg_id).encode()).hexdigest()
        sql_query = insert(VPNUsers).values(tg_id=tg_id, vpn_id=hash)
        await conn.execute(sql_query)
        await conn.commit()

async def get_marzban_profile_db(tg_id: int) -> VPNUsers:
    async with engine.connect() as conn:
        sql_query = select(VPNUsers).where(VPNUsers.tg_id == tg_id)
        result: VPNUsers = (await conn.execute(sql_query)).fetchone()
    return result

async def get_marzban_profile_by_vpn_id(vpn_id: str):
    async with engine.connect() as conn:
        sql_query = select(VPNUsers).where(VPNUsers.vpn_id == vpn_id)
        result: VPNUsers = (await conn.execute(sql_query)).fetchone()
    return result    

async def can_get_test_sub(tg_id: int) -> bool:
    async with engine.connect() as conn:
        sql_query = select(VPNUsers).where(VPNUsers.tg_id == tg_id)
        result: VPNUsers = (await conn.execute(sql_query)).fetchone()
    return result.test

async def update_test_subscription_state(tg_id):
    async with engine.connect() as conn:
        sql_q = update(VPNUsers).where(VPNUsers.tg_id == tg_id).values(test=True)
        await conn.execute(sql_q)
        await conn.commit()

async def add_yookassa_payment(tg_id: int, callback: str, chat_id: int, lang_code: str, payment_id) -> dict:
    async with engine.connect() as conn:
        sql_q = insert(YPayments).values(tg_id=tg_id, payment_id=payment_id, chat_id=chat_id, callback=callback, lang=lang_code)
        await conn.execute(sql_q)
        await conn.commit()

async def add_cryptomus_payment(tg_id: int, callback: str, chat_id: int, lang_code: str, data) -> dict:
    async with engine.connect() as conn:
        sql_q = insert(CPayments).values(tg_id=tg_id, payment_uuid=data['order_id'], order_id=data['order_id'], chat_id=chat_id, callback=callback, lang=lang_code)
        await conn.execute(sql_q)
        await conn.commit()

async def get_yookassa_payment(payment_id) -> YPayments:
    async with engine.connect() as conn:
        sql_q = select(YPayments).where(YPayments.payment_id == payment_id)
        payment: YPayments = (await conn.execute(sql_q)).fetchone()
    return payment

async def get_cryptomus_payment(order_id) -> CPayments:
    async with engine.connect() as conn:
        sql_q = select(CPayments).where(CPayments.order_id == order_id)
        payment: CPayments = (await conn.execute(sql_q)).fetchone()
    return payment

async def delete_payment(payment_id):
    async with engine.connect() as conn:
        sql_q = delete(YPayments).where(YPayments.payment_id == payment_id)
        await conn.execute(sql_q)
        await conn.commit()
        sql_q = delete(CPayments).where(CPayments.payment_uuid == payment_id)
        await conn.execute(sql_q)
        await conn.commit()