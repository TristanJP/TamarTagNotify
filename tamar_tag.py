import appdirs
import json
import os
import requests
import telegram_send

from bs4 import BeautifulSoup

class TamarTag:

    URL = 'https://tags.tamarcrossings.org.uk/index.php'
    config_path = os.path.join(appdirs.user_config_dir("tamar_tag"), 'config.json')

    def __init__(self):
        if os.path.exists(self.config_path):
            with open(self.config_path) as cf:
                self.config = json.load(cf)
        else:
            print(f"No config file found: {self.config_path}")
            exit(1)

    def login(self):
        params = {
            "MODULE": "actions",
            "acClase": "login",
            "acMetodo": "acLogin",
            "acTipo": "ajax",
            "username": self.config["username"],
            "password": self.config["password"],
            "postcode1": self.config["postcode1"],
            "postcode2": self.config["postcode2"]
        }
        try:
            resp = self.session.get(self.URL, params=params)
        except Exception as ce:
            print(f"Login failed - Could not connect to URL: {self.URL}\n{ce}")
            exit(1)
        return resp.status_code == requests.codes.ok

    def logout(self):
        params = {
            "MODULE": "actions",
            "acClase": "Home",
            "acMetodo": "acLogout",
            "acTipo": "std"
        }
        resp = self.session.get(self.URL, params=params)
        return resp.status_code == requests.codes.found

    def get_current_credit(self):
        params = {
            "page": "topUpAccount"
        }
        resp = self.session.get(self.URL, params=params)
        return int(BeautifulSoup(resp.text, "html.parser").find('input', class_='form-control')['value'])

    def warn(self, current_credit):
        telegram_send.send(messages=[f"Tamar Tag credit is getting low: {current_credit}"])

    def main(self):
        with requests.Session() as self.session:
            if self.login():
                current_credit = self.get_current_credit()
                if current_credit <= self.config['minimum']:
                    self.warn(current_credit)
                self.logout()


if __name__ == '__main__':
    tt = TamarTag()
    tt.main()
