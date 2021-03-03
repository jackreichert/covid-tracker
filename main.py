import requests
import sys
import random
import smtplib
import os
import time


class CovidChecker:
    def __init__(self):
        self.sender_address = os.environ.get('GMAIL_UN')
        self.account_password = os.environ.get('GMAIL_PW')
        self.receiver_address = os.environ.get('GMAIL_UN')
        self.stores = []
        self.timer = int(time.time())

    def send_email(self, subject='', body=''):
        print("sending email...")
        smtp_server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtp_server.login(self.sender_address, self.account_password)
        message = f"Subject: {subject}\n\n{body}"
        smtp_server.sendmail(self.sender_address, self.receiver_address, message)
        smtp_server.close()

    def get_sleeptime(self):
        return random.randrange(1, 5)

    def wait_retry(self, sleep_time):
        print(f"Waiting {int(sleep_time / 60)} minutes {sleep_time % 60} seconds to try again.\n\n")
        time.sleep(sleep_time)
        self.check()

    def should_loop(self):
        return 'loop=True' in sys.argv

    def has_mintes_elapesd(self):
        return int(time.time()) > self.timer + 300

    def reset(self):
        self.timer = int(time.time())
        self.stores = []

    def check(self):
        zip = sys.argv[1]
        nearby_stores_url = f"https://www.riteaid.com/services/ext/v2/stores/getStores?address={zip}&attrFilter=PREF-112&fetchMechanismVersion=2&radius=50";
        appointment_availability_url = f"https://www.riteaid.com/services/ext/v2/vaccine/checkSlots?storeNumber=";

        stores_response = requests.get(nearby_stores_url).json()
        sleep_time = self.get_sleeptime()
        storelen = len(self.stores)
        for store in stores_response['Data']['stores']:
            availability_response = requests.get(appointment_availability_url + str(store['storeNumber'])).json()
            if store in self.stores and availability_response['Status'] == 'SUCCESS' \
                    and not availability_response['Data']['slots']['1'] \
                    and not availability_response['Data']['slots']['2']:
                self.reset()
                self.check()

            if availability_response['Status'] == 'SUCCESS' \
                    and (availability_response['Data']['slots']['1'] or availability_response['Data']['slots']['2']):
                if store not in self.stores:
                    self.stores.append(store)
        if len(self.stores):
            subject = f'Covid-19 Vaccine Appointments Available!'
            body = 'Schedule here: https://www.riteaid.com/pharmacy/covid-qualifier\n'
            for store in self.stores:
                body += f'Appointment available at store #{store["storeNumber"]}, {store["locationDescription"]}, phone: {store["fullPhone"]}, distance: {store["milesFromCenter"]}\n'
            print(body)
            if self.should_loop():
                if storelen < len(self.stores):
                    self.send_email(subject, body)
                if self.has_mintes_elapesd():
                    self.reset()
        else:
            print("No appointments available nearby.")
        if self.should_loop():
            self.wait_retry(sleep_time)


def main():
    checker = CovidChecker()
    checker.check()


if __name__ == '__main__':
    main()
