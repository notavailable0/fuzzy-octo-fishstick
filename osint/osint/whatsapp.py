import requests
import json

import asyncio
import aiohttp

url = 'https://w2.checkwa.com/check/'

## TODO SENTRY
## todo timeout fix, test limits of checkwa
## todo sqlalchemy
## tood different responses diff usage

async def cwablk():
    tasks_list = []
    results = []

    #достать с бд
    with open("input_data.txt", "r") as db:
        txt_data_strings = db.read()

    json_data_strings = json.loads(txt_data_strings)

    numbers = [str(string["phone"]) for string in json_data_strings] ## 100 шт, которые залетают

    connector = aiohttp.TCPConnector(limit=3)

    async with aiohttp.ClientSession(connector=connector) as session:
        for number in numbers:

            payload = json.dumps({
                "user": "theowll",
                "apikey": "43fd05-f190cc-0bfed7-26745e-b58da8",
                "number": number
            })

            headers = {
                'Content-Type': 'application/json'
            }

            tasks_list.append(asyncio.create_task(session.post(url, data=payload, headers=headers)))

        responses = await asyncio.gather(*tasks_list)
        for response in responses:
            results.append(await response.json())

    ## filter responses for timed out etc 
    ## log the fuck out of this code

    return results


if __name__ == "__main__":
    print(asyncio.run(cwablk()))
