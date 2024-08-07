import asyncio
import requests
import json
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
    response = requests.post(url, headers=headers, json=body)
    response_data = json.loads(response.content.decode('utf-8'))
    if response_data.get("status") == "CLAIMABLE":
        return response_data
    else:
        return(response_data["status"])
    
async def main_async():
    if os.path.isfile("bearertoken.txt") and os.stat("bearertoken.txt").st_size != 0:
        myfile = open("bearertoken.txt",'r')
        token = (myfile.read())
        myfile.close()
    else:
        token = str(input("Input Bearer token: "))
        
    if os.path.isfile("cccodes.txt") and os.stat("cccodes.txt").st_size != 0:
        timeout = {'message': 'Too Many Requests', 'status_code': 429}
        myfile = open("cccodes.txt",'r')
        for line in myfile:
            cc = (line.strip('\n'))
            print("Checking:",cc)
            contents = await check(token, cc)
            print(contents)
            while contents == timeout:
                print("Waiting and retrying:",cc)
                await asyncio.sleep(7)
                contents = await check(token, cc)
                print(contents)
            await asyncio.sleep(7)    
        myfile.close()
    else:
        num_times = int(input("How many codes do you want to check? "))
        for _ in range(num_times):
            cc = str(input("Input CC code: "))
            contents = await check(token, cc)
            print(contents)
    
if __name__ == "__main__":
    asyncio.run(main_async())