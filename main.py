import requests
import sys
import time
import random
import smtplib
import os


def send_email(subject='', body=''):
    sender_address = os.environ.get('GMAIL_UN')
    receiver_address = os.environ.get('GMAIL_UN')
    account_password = os.environ.get('GMAIL_PW')

    smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    smtp_server.login(sender_address, account_password)
    message = f"Subject: {subject}\n\n{body}"
    smtp_server.sendmail(sender_address, receiver_address, message)
    smtp_server.close()


def get_sleeptime(multiplier=1):
    sleep_time = 0
    sleep_time += (random.randrange(5)) * 60
    sleep_time += random.randrange(60)
    sleep_time *= multiplier
    return sleep_time


def wait_retry(sleep_time):
    print(f"Waiting {int(sleep_time / 60)} minutes {sleep_time % 60} seconds to try again.")
    time.sleep(sleep_time)
    main()


def should_loop():
    return 'loop=True' in sys.argv


def main():
    zip = sys.argv[1]
    nearby_stores_url = f"https://www.riteaid.com/services/ext/v2/stores/getStores?address={zip}&attrFilter=PREF-112&fetchMechanismVersion=2&radius=50";
    appointment_availability_url = f"https://www.riteaid.com/services/ext/v2/vaccine/checkSlots?storeNumber=";

    stores_response = requests.get(nearby_stores_url).json()
    sleep_time = get_sleeptime()
    stores = []
    for store in stores_response['Data']['stores']:
        availability_response = requests.get(appointment_availability_url + str(store['storeNumber'])).json()
        if availability_response['Data']['slots']['1'] or availability_response['Data']['slots']['2']:
            stores.append(store)
    if len(stores):
        body = 'Schedule here: https://www.riteaid.com/pharmacy/covid-qualifier\n\n'
        for store in stores:
            subject = f'Covid-19 Vaccine Appointments Available!'
            body += f'Appointment available at store #{store["storeNumber"]}, {store["locationDescription"]}, phone: {store["fullPhone"]}, distance: {store["milesFromCenter"]}\n\n'
        print(body)
        if should_loop():
            body += f"\n will try again in {int(sleep_time / 60)} minutes {sleep_time % 60} seconds"
            send_email(subject, body)
    else:
        print("No appointments available nearby.")
    if should_loop():
        wait_retry(sleep_time)


if __name__ == '__main__':
    main()
