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

    # Load TDesktop client from tdata folder
    tdataFolder = r"C:\Users\fuck ur mum\Desktop\whatsapp & co\osint\osint\accounts\tg_accs_not_used\13375109677\tdata"
    # us2.4g.iproyal.com:7044:nnCCF1S:qYucGAlsM0KIqxw
    tdesk = TDesktop(tdataFolder)

##    us2.4g.iproyal.com:7044:nnCCF1S:qYucGAlsM0KIqxw
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



    with open("input_data.txt", "r") as db:
        txt_data_strings = db.read()

    json_data_strings = json.loads(txt_data_strings)

    numbers = [string for string in json_data_strings] ## условная замена бд
    contacts = []
    count = 0

    for n in numbers:

        contact = types.InputPhoneContact(
            client_id=0,
            phone=str(n['phone']),
            first_name="baby",
            last_name=""
        )

        contacts = await client(functions.contacts.ImportContactsRequest([contact]))

        users = contacts.to_dict().get("users", [])
        number_of_matches = len(users)


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
        count += 1

    results = await client(functions.contacts.GetContactsRequest(
        hash=0
    ))
    print(results.stringify())


    await client.disconnect()
    return has_tg

asyncio.run(main())
print("finished")