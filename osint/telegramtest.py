import asyncio
import json
import os
import re
import random
import string

from telethon.sync import TelegramClient, errors, functions
from telethon.tl import types
from telethon.sessions import Session

from opentele.td import TDesktop
from opentele.tl import TelegramClient
from opentele.api import API, CreateNewSession, UseCurrentSession

def create_random_names() -> str: return ''.join(random.choices(string.ascii_uppercase, k=5))

async def main():
    has_tg = []

    # папка с тдата, зависит от поставщика, кто в тдата кто в сессии
    tdataFolder = r"accounts\tg_accs_not_used\13375109677\tdata" # тут хардкод, экономил время, надо чтоб с бд тянулась локация и находился файл

    tdesk = TDesktop(tdataFolder) # враппер телетона для распаковки тдата формата, отличается только этой строкой и наличием юашек, лучше для спама

    # сокс 5 прокся : us2.4g.iproyal.com:3044:nnCCF1S:qYucGAlsM0KIqxw
    proxy = {
    'proxy_type': 'socks5', # (mandatory) protocol to use (see above)
    'addr': 'us2.4g.iproyal.com',      # (mandatory) proxy IP address
    'port': 3044,           # (mandatory) proxy port number
    'username': 'nnCCF1S',      # (optional) username if the proxy requires auth
    'password': 'qYucGAlsM0KIqxw',      # (optional) password if the proxy requires auth
    }

    client = await tdesk.ToTelethon("newSession5.session", UseCurrentSession, proxy=proxy)
    await client.connect()
    await client.PrintSessions()

    with open("input_data.txt", "r") as db: # симуляция базы, рандомные номера
        txt_data_strings = db.read()

    json_data_strings = json.loads(txt_data_strings)

    numbers = [string for string in json_data_strings] ## условная замена бд, не нужный код, оставил чтоб не ломать
    contacts = []

    for count, n in enumerate(numbers):

        contact = types.InputPhoneContact(
            client_id=0,
            phone=str(n['phone']),
            # телефон
            first_name="павел",
            last_name="ебуров"
        )
        try:
            contacts = await client(functions.contacts.ImportContactsRequest([contact]))
        except errors.TakeoutInitDelayError as e:
            print('Must wait', e.seconds, 'before takeout')
            await client.disconnect()
            await asyncio.sleep(e.seconds)
            ## отоспаться на куллдауне надо расширить этот трай на остальные методы, либо на всю функцию

        users = contacts.to_dict().get("users", []) # если не [], есть тг
        number_of_matches = len(users)

        #results = await client(functions.contacts.GetContactsRequest(hash=0))
        # хеш 0, должен отдавать все контакты акка. можно для балк-чека юзать, тут по 10 за раз, лимит 5к
        # отдает не только телефон, юзернейм итд.
        #[{'_': 'User', 'id': 1346492764, 'is_self': False, 'contact': True, 'mutual_contact': False, 'deleted': False, 'bot': False, 'bot_chat_history': False, 'bot_nochats': False, 'verified': False, 'restricted': False, 'min': False, 'bot_inline_geo': False, 'support': False, 'scam': False, 'apply_min_photo': True, 'fake': False, 'bot_attach_menu': False, 'premium': False, 'attach_menu_enabled': False, 'bot_can_edit': False, 'close_friend': False, 'stories_hidden': False, 'stories_unavailable': True, 'contact_require_premium': False, 'bot_business': False, 'access_hash': -2157636302422222132, 'first_name': 'павел', 'last_name': 'ебуров', 'username': 'KI7YLZ', 'phone': '15033188531', 'photo': None, 'status': {'_': 'UserStatusLastMonth', 'by_me': False}, 'bot_info_version': None, 'restriction_reason': [], 'bot_inline_placeholder': None, 'lang_code': None, 'emoji_status': None, 'usernames': [], 'stories_max_id': None, 'color': None, 'profile_color': None}]

        #print(results.stringify())

        if number_of_matches == 0:
            # сообщение о отсутствии телеги
            pass

        elif number_of_matches == 1:
            has_tg.append(n)

        else:
            pass
            #закинуть в бд сообщение о непонятных движках


        print(users)
        print(count)

        if count == 49: # лимит телеги 50 за раз, в целом 5к куллдаун 5мин, акк надо заносить в бд как в "куллдаун", потом сделаю
            await client.disconnect()
            return has_tg

    return has_tg

asyncio.run(main())