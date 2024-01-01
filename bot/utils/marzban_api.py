import time
import aiohttp
import requests

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
            "method": "chacha20-ietf-poly1305"
        },
        ["Shadowsocks TCP"]
    ]
}

class Marzban:
    def __init__(self, ip, login, passwd) -> None:
        self.ip = ip
        self.login = login
        self.passwd = passwd
    
    async def _send_request(self, method, path, headers=None, data=None) -> dict | list:
        async with aiohttp.ClientSession() as session:
            async with session.request(method, self.ip + path, headers=headers, json=data) as resp:
                if 200 <= resp.status < 300:
                    body = await resp.json()
                    return body
                else:
                    raise Exception(f"Error: {resp.status}; Body: {await resp.text()}; Data: {data}")
    
    def get_token(self) -> str:
        data = {
            "username": self.login,
            "password": self.passwd
        }
        resp = requests.post(self.ip + "/api/admin/token", data=data).json()
        self.token = resp["access_token"]
        return self.token
    
    async def get_user(self, username) -> dict:
        headers = {
            'Authorization': f"Bearer {self.token}"
        }
        resp = await self._send_request("GET", f"/api/user/{username}", headers=headers)
        return resp
    
    async def get_users(self) -> dict:
        headers = {
            'Authorization': f"Bearer {self.token}"
        }
        resp = await self._send_request("GET", "/api/users", headers=headers)
        return resp
    
    async def add_user(self, data) -> dict:
        headers = {
            'Authorization': f"Bearer {self.token}"
        }
        resp = await self._send_request("POST", "/api/user", headers=headers, data=data)
        return resp
    
    async def modify_user(self, username, data) -> dict:
        headers = {
            'Authorization': f"Bearer {self.token}"
        }
        resp = await self._send_request("PUT", f"/api/user/{username}", headers=headers, data=data)
        return resp

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

panel = Marzban(glv.config['PANEL_HOST'], glv.config['PANEL_USER'], glv.config['PANEL_PASS'])
mytoken = panel.get_token()
ps = get_protocols()

async def check_if_user_exists(name: str) -> bool:
    try:
        await panel.get_user(name)
        return True
    except Exception as e:
        return False

async def get_marzban_profile(tg_id: int):
    result = await get_marzban_profile_db(tg_id)
    res = await check_if_user_exists(result.vpn_id)
    if not res:
        return None
    return await panel.get_user(result.vpn_id)

async def generate_test_subscription(username: str):
    res = await check_if_user_exists(username)
    if res:
        user = await panel.get_user(username)
        user['status'] = 'active'
        if user['expire'] < time.time():
            user['expire'] = get_test_subscription(glv.config['PERIOD_LIMIT'])
        else:
            user['expire'] += get_test_subscription(glv.config['PERIOD_LIMIT'], True)
        result = await panel.modify_user(username, user)
    else:
        user = {
            'username': username,
            'proxies': ps["proxies"],
            'inbounds': ps["inbounds"],
            'expire': get_test_subscription(glv.config['PERIOD_LIMIT']),
            'data_limit': 0,
            'data_limit_reset_strategy': "no_reset",
        }
        result = await panel.add_user(user)
    return result

async def generate_marzban_subscription(username: str, good):
    res = await check_if_user_exists(username)
    if res:
        user = await panel.get_user(username)
        user['status'] = 'active'
        if user['expire'] < time.time():
            user['expire'] = get_subscription_end_date(good['months'])
        else:
            user['expire'] += get_subscription_end_date(good['months'], True)
        result = await panel.modify_user(username, user)
    else:
        user = {
            'username': username,
            'proxies': ps["proxies"],
            'inbounds': ps["inbounds"],
            'expire': get_subscription_end_date(good['months']),
            'data_limit': 0,
            'data_limit_reset_strategy': "no_reset",
        }
        result = await panel.add_user(user)
    return result

def get_test_subscription(hours: int, additional= False) -> int:
    return (0 if additional else int(time.time())) + 60 * 60 * hours

def get_subscription_end_date(months: int, additional = False) -> int:
    return (0 if additional else int(time.time())) + 60 * 60 * 24 * 30 * months
