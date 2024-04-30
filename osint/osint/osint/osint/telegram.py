import asyncio
import json
import os
import re
import random
import string

from telethon.sync import TelegramClient, errors, functions
from telethon.tl import types
from telethon.sessions import Session

# 5 - 6 потоков, номера чекать до лимита тг как понять когда лимит?
# речек акка на жизнеспособность после круга отработки, в бд как поюзанный акк

def create_random_names() -> str: return ''.join(random.choices(string.ascii_uppercase, k=5))

async def get_names(data : list, tg_accounts : list, proxies : list) -> list:
    has_tg = []

    for number in numbers:
        try:
            tg_account = tg_accounts[0]
            API_ID = tg_account["api_id"]
            API_HASH = tg_account["api_hash"]
            PHONE_NUMBER = tg_account["phone_number"]
            SESSION_STRING = tg_account["sesion"]
            client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

            await client.connect()

            if not await client.is_user_authorized():
                #await client.send_code_request(PHONE_NUMBER) логин без челленджей
                try:
                    await client.sign_in(
                        PHONE_NUMBER, input("Enter the code (sent on telegram): ")
                    )
                except errors.SessionPasswordNeededError:
                    pw = getpass(
                        "Two-Step Verification enabled. Please enter your account password: "
                    )

            # await client.sign_in(password=pw) 2фа не желательна, можно потом посмотреть

            contact = types.InputPhoneContact(
                client_id=0, phone=phone_number, first_name=create_random_names(), last_name=create_random_names()
            )

            contacts = await client(functions.contacts.ImportContactsRequest([contact]))

            users = contacts.to_dict().get("users", [])
            number_of_matches = len(users)

            if number_of_matches == 0:
                # сообщение о отсутствии телеги
                pass

            elif number_of_matches == 1:
                has_tg.append(number)

            else:
                pass
                #закинуть в бд сообщение о непонятных движках

        except TypeError as e:
            # логги
            print(e)

        except Exception as e:
            # логги
            print(e)

    return result

if __name__ == "__main__":
    #достать с бд
    with open("input_data.txt", "r") as db:
        txt_data_strings = db.read()

    json_data_strings = json.loads(txt_data_strings)

    numbers = [string for string in json_data_strings] ## условная замена бд


##    with open("accounts/telegram_accounts.txt","r") as ta:
##        txt_data_strings = ta.read()
##
##    json_data_strings = json.loads(txt_data_strings)
##
##    accounts = [string for string in json_data_strings] ## условная замена бд

    tg_accs_dir = os.listdir("accounts/tg_accs_not_used")
    tdatalinks = [f"accounts/tg_accs_not_used/{accfolder}" for accfolder in tg_accs_dir]

    with open("accounts/proxies.txt","r") as ta:
        txt_data_strings = ta.read()

    json_data_strings = json.loads(txt_data_strings)

    proxies = [string for string in json_data_strings] ## условная замена бд
    # формат проксей

    asyncio.run(get_names(numbers, accounts, proxies))

