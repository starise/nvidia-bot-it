import json
import platform
import random
import webbrowser
from datetime import datetime, time
from os import path, getenv, system
from time import sleep
import sys
import requests
from dotenv import load_dotenv

platform = platform.system()
OS_WIN = "Windows"
OS_LIN = "Linux"
OS_MAC = "Darwin"

# Set up environment variables and constants.
load_dotenv()
USE_TWILIO = False
TWILIO_TO_NUM = getenv('TWILIO_TO_NUM')
TWILIO_FROM_NUM = getenv('TWILIO_FROM_NUM')
TWILIO_SID = getenv('TWILIO_SID')
TWILIO_AUTH = getenv('TWILIO_AUTH')
ALERT_DELAY = int(getenv('ALERT_DELAY'))
MIN_DELAY = int(getenv('MIN_DELAY'))
MAX_DELAY = int(getenv('MAX_DELAY'))
OPEN_WEB_BROWSER = getenv('OPEN_WEB_BROWSER') == 'true'

with open('sites.json', 'r') as f:
    sites = json.load(f)


# Twilio Setup
if TWILIO_TO_NUM and TWILIO_FROM_NUM and TWILIO_SID and TWILIO_AUTH:
    USE_TWILIO = True

    print("Configurazione di Twilio in corso... ", end='')

    from twilio.rest import Client
    client = Client(TWILIO_SID, TWILIO_AUTH)

    print("OK!")


# Platform specific settings
print("Sistema operativo: {}".format(platform))
if platform == OS_WIN:
    from win10toast import ToastNotifier
    toast = ToastNotifier()


def is_test():
    try:
        if sys.argv[1] == 'test':
            send_alert(sites[0])
            print("Test completato. Se hai ricevuto le notifiche sei a posto! :)")
            return True
    except:
        return False

def get_status(site):
    url = site.get('url')
    api_url = site.get('api')
    response = requests.get(api_url, timeout=5)
    return response.json()


def send_alert(site):
    product = site.get('name')
    print("{} DISPONIBILE".format(product))
    print(site.get('url'))
    if OPEN_WEB_BROWSER:
        webbrowser.open(site.get('url'), new=1)
    os_notification("{} DISPONIBILE".format(product), site.get('url'))
    sms_notification("DISPONIBILE: ", site.get('url'))


def os_notification(title, text):
    if platform == OS_MAC:
        system("""
                  osascript -e 'display notification "{}" with title "{}"'
                  """.format(text, title))
        system('afplay /System/Library/Sounds/Glass.aiff')
        system('say "{}"'.format(title))
    elif platform == OS_WIN:
        toast.show_toast(title, text, duration=5, icon_path="favicon.ico")
    elif platform == OS_LIN:
        # TODO
        pass


def sms_notification(url):
    if USE_TWILIO:
        client.messages.create(to=TWILIO_TO_NUM, from_=TWILIO_FROM_NUM, body=url)


def main():

    exit() if is_test() else False

    search_count = 1

    while True:
        current_time = datetime.now().strftime("%H:%M:%S")

        print("\n[{}] TENTATIVO # {}".format(current_time, search_count))
        search_count += 1

        for site in sites:
            if site.get('enabled'):

                try:
                    item = get_status(site)
                except Exception as e:
                    print("[!]  CONNESSIONE FALLITA: {}".format(e))
                    continue

                print("- PRODOTTO: \t {}".format(item['products']['product'][0]['displayName']))

                if item['products']['product'][0]['inventoryStatus']['status'] != "PRODUCT_INVENTORY_OUT_OF_STOCK":
                    print("  STATO: \t {}".format("DISPONIBILE!!"))
                    send_alert(site)
                    sleep(ALERT_DELAY)
                else:
                    print("  STATO: \t PRODOTTO ESAURITO")

        sleep(1 + random.uniform(MIN_DELAY, MAX_DELAY))


if __name__ == '__main__':
    main()
