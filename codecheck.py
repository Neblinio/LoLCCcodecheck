import asyncio
import requests
import json

async def check(bearer_token, code):
    url = "https://usw2-red.pp.sgp.pvp.net/contentcodes/v1/validate"
    
    headers = {
    "Authorization": f"Bearer {bearer_token}"
    }
    
    body = {
        "code": code,
        "locale": "en_US"
    }
    response = requests.post(url, headers=headers, json=body)
    response_data = json.loads(response.content.decode('utf-8'))
    if response_data.get("status") == "CLAIMABLE":
        return response_data
    else:
        return(response_data["status"])
    
async def main_async():
    token = str(input("Input Bearer token: "))
    num_times = int(input("How many codes do you want to check? "))
    for _ in range(num_times):
        cc = str(input("Input CC code: "))
        contents = await check(token, cc)
        print(contents)
    
if __name__ == "__main__":
    asyncio.run(main_async())