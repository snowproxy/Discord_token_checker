import requests
import json
import threading
from colorama import Fore

class Discord:
    def __init__(self, token):
        self.full_token = token
        token = token.split(":")
        tokens = token[2]
        self.token = tokens
        self.session = requests.Session()
        self.session.headers.update({
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.8",
            "authorization": self.token,
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://discord.com/",
            "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
        })

    def get_cookies(self):
        response = self.session.get("https://discord.com/", proxies=proxies)
        return response.cookies
    
    def check_token(self):
        response = self.session.get("https://discord.com/api/v9/users/@me/library", cookies=self.get_cookies(), proxies=proxies)
        if response.status_code == 200:
            print(f"{Fore.GREEN}[+] Valid token: {Fore.BLUE}{self.token}")
            with open("good.txt", "a") as file:
                file.write(f"{self.full_token}\n")
        elif response.status_code == 401:
            print(f"{Fore.RED}[-] Invalid token: {Fore.BLUE}{self.token}")
            with open("bad.txt", "a") as file:
                file.write(f"{self.full_token}\n")

tokens = []
lock = threading.Lock()

def worker():
    while True:
        lock.acquire()
        if tokens:
            token = tokens.pop()
            lock.release()
            discord = Discord(token)
            discord.check_token()
        else:
            lock.release()
            break

def main():
    global tokens
    global proxies
    proxies = {
        "http": "http://user:pass@proxy.snowproxies.digital:13134"
    }
    with open("tokens.txt", "r") as file:
        tokens = [line.strip() for line in file.readlines()]

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()