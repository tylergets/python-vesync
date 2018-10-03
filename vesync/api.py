import requests
import hashlib
import json

requests.packages.urllib3.disable_warnings()

BASE_URL = "https://smartapi.vesync.com"

class VesyncApi:
    def __init__(self, username, password):
        payload = json.dumps({"account":username,"devToken":"","password":hashlib.md5(password.encode('utf-8')).hexdigest()})
        account = requests.post(BASE_URL + "/vold/user/login", verify=False, data=payload).json()
        if "error" in account:
            raise RuntimeError("Invalid username or password")
        else:
            self._account = account
        self._devices = []

    def get_devices(self):
        self._devices = requests.get(BASE_URL + '/vold/user/devices', verify=False, headers=self.get_headers()).json()
        return self._devices

    def get_config(self, id):
        self._configuration = requests.get(BASE_URL + '/v1/device/' + id + '/configurations', verify=False, headers=self.get_headers()).json()
        return self._configuration

    def get_detail(self, id):
        self._detail = requests.get(BASE_URL + '/v1/device/' + id + '/detail', verify=False, headers=self.get_headers()).json()
        return self._detail

    def turn_on(self, id):
        requests.put(BASE_URL + '/v1/wifi-switch-1.3/' + id + '/status/on', verify=False, data={}, headers=self.get_headers())

    def turn_off(self, id):
        requests.put(BASE_URL + '/v1/wifi-switch-1.3/' + id + '/status/off', verify=False, data={}, headers=self.get_headers())

    def get_headers(self):
        return {'tk':self._account["tk"],'accountid':self._account["accountID"]}
