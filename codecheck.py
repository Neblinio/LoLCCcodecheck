import asyncio
import httpx
import os

async def check(bearer_token, code):
    url = "https://usw2-red.pp.sgp.pvp.net/contentcodes/v1/validate"
    
    headers = {
    "Authorization": f"Bearer {bearer_token}"
    }
    
    body = {
        "code": code,
        "locale": "en_US"
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        return response
    
async def main_async():
    if os.path.isfile("bearertoken.txt") and os.stat("bearertoken.txt").st_size != 0:
        with open("bearertoken.txt", 'r') as myfile:
            token = myfile.read().strip()
    else:
        token = str(input("Input Bearer token: "))
        
    if os.path.isfile("cccodes.txt") and os.stat("cccodes.txt").st_size != 0:
        with open("cccodes.txt", 'r') as myfile:
            for line in myfile:
                cc = line.strip()
                print("Checking:",cc)
                contents = await check(token, cc)
                print(contents.json())
                while contents.status_code == 429:
                    print("Waiting and retrying:",cc)
                    await asyncio.sleep(7)
                    contents = await check(token, cc)
                    print(contents.json())
                await asyncio.sleep(7)
    else:
        num_times = int(input("How many codes do you want to check? "))
        for _ in range(num_times):
            cc = str(input("Input CC code: "))
            contents = await check(token, cc)
            print(contents.json())
    
if __name__ == "__main__":
    asyncio.run(main_async())