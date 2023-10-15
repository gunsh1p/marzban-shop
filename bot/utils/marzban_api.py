from marzpy import Marzban
import time

def check_if_exists(name: str, panel: Marzban) -> bool:
    token = panel.get_token()
    users = panel.get_all_users(token)
    for user in users:
        if user.username == name:
            return True
    return False

def get_test_subscription(days: int, additional= False) -> int:
    return (0 if additional else int(time.time())) + 60 * 60 * 24 * days

def get_subscription_end_date(months: int, additional = False) -> int:
    return (0 if additional else int(time.time())) + 60 * 60 * 24 * 30 * months