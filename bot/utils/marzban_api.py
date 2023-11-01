import time

from marzpy import Marzban
from marzpy.api.user import User

from db.methods import get_marzban_profile_db
import glv

PROTOCOLS = {
    "vmess": [
        {},
        ["VMess TCP"]
    ],
    "vless": [
        {
            "flow": "xtls-rprx-vision"
        },
        ["VLESS TCP REALITY"]
    ],
    "trojan": [
        {},
        ["Trojan Websocket TLS"]
    ],
    "shadowsocks": [
        {
            "method": "chacha20-poly1305"
        },
        ["Shadowsocks TCP"]
    ]
}

def get_protocols() -> dict:
    proxies = {}
    inbounds = {}
    
    for proto in glv.config['PROTOCOLS']:
        l = proto.lower()
        if l not in PROTOCOLS:
            continue
        proxies[l] = PROTOCOLS[l][0]
        inbounds[l] = PROTOCOLS[l][1]
    return {
        "proxies": proxies,
        "inbounds": inbounds
    }

panel = Marzban(glv.config['PANEL_USER'], glv.config['PANEL_PASS'], glv.config['PANEL_HOST'])
mytoken = panel.get_token()
ps = get_protocols()

def check_if_user_exists(name: str) -> bool:
    try:
        panel.get_user(name, mytoken)
        return True
    except:
        return False

async def get_marzban_profile(tg_id: int) -> User:
    result = await get_marzban_profile_db(tg_id)
    if not check_if_user_exists(result.vpn_id):
        return None
    return panel.get_user(result.vpn_id, mytoken)

def generate_test_subscription(username: str) -> User:
    if check_if_user_exists(username):
        user = panel.get_user(username, mytoken)
        user.status = 'active'
        if user.expire < time.time():
            user.expire = get_test_subscription(glv.config['PERIOD_LIMIT'])
        else:
            user.expire += get_test_subscription(glv.config['PERIOD_LIMIT'], True)
        result: User = panel.modify_user(username, mytoken, user)
    else:
        user = User(
            username=username,
            proxies=ps["proxies"],
            inbounds=ps["inbounds"],
            expire=get_test_subscription(glv.config['PERIOD_LIMIT']),
            data_limit=0,
            data_limit_reset_strategy="no_reset",
        )
        result: User = panel.add_user(user=user, token=mytoken)
    return result

def generate_marzban_subscription(username: str, good) -> User:
    if check_if_user_exists(username):
        user = panel.get_user(username, mytoken)
        user.status = 'active'
        if user.expire < time.time():
            user.expire = get_subscription_end_date(good['months'])
        else:
            user.expire += get_subscription_end_date(good['months'], True)
        result = panel.modify_user(username, mytoken, user)
    else:
        user = User(
            username=username,
            proxies=ps["proxies"],
            inbounds=ps["inbounds"],
            expire=get_subscription_end_date(good['months']),
            data_limit=0,
            data_limit_reset_strategy="no_reset",
        )
        result = panel.add_user(user=user, token=mytoken)
    return result

def get_test_subscription(days: int, additional= False) -> int:
    return (0 if additional else int(time.time())) + 60 * 60 * 24 * days

def get_subscription_end_date(months: int, additional = False) -> int:
    return (0 if additional else int(time.time())) + 60 * 60 * 24 * 30 * months