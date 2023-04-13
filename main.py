import requests
import telegram
import time
import python-telegram-bot
from telegram.ext import Updater, CommandHandler
print("Telegram Proxy scraper by Jitski.")
# Replace with your own Telegram bot token and chat ID
BOT_TOKEN = 'YOUR_TOKEN'
CHAT_ID = 'YOUR_CHAT_ID'

def get_proxies():
    # URLs to retrieve proxies from
    urls = {
        'http': 'https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=1000&country=all',        # change the timout if you want
        'https': 'https://api.proxyscrape.com/?request=getproxies&proxytype=https&timeout=1000&country=all',
        'socks4': 'https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=1000&country=all',
        'socks5': 'https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=1000&country=all',
    }
    proxies = {}

    # Retrieve proxies from URLs
    for key, url in urls.items():
        response = requests.get(url)
        if response.status_code == 200:
            proxies[key] = response.text.strip().split('\n')
        else:
            proxies[key] = []

    return proxies

def upload_proxies():
    while True:
        # Get proxies
        proxies = get_proxies()

        # Upload proxies to Telegram chat
        bot = telegram.Bot(token=BOT_TOKEN)
        for key, proxy_list in proxies.items():
            if proxy_list:
                # Create a text file with the proxy list
                with open(f'{key}_jitski.txt', 'w') as f:
                    f.write('\n'.join(proxy_list))
                # Upload the text file to the Telegram chat
                with open(f'{key}_jitski.txt', 'rb') as f:
                    bot.send_document(chat_id=CHAT_ID, document=f, filename=f.name)
        
        # Wait for 3000 seconds(50 mins) before uploading the proxies again
        time.sleep(3000)
                
if __name__ == '__main__':
    # Call the function to upload the proxies to the Telegram chat
    upload_proxies()
