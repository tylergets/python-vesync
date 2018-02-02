import requests
import hashlib
import json

requests.packages.urllib3.disable_warnings()
BASE_URL = "https://server1.vesync.com:4007"

class VesyncApi:
    
    """
    init and log into vesync with credentials
    """
    def __init__(self, username, password):
        self.session = requests.Session()
        data = {
            'Account': username,
            'Password': hashlib.md5(password.encode('utf-8')).hexdigest(),
        }
        headers = {
            "account": username,
            "password": hashlib.md5(password.encode('utf-8')).hexdigest(),
        }
        req = requests.Request(
            'POST',
            BASE_URL + "/login",
            json=data,
            headers=headers,
        )
        prepared = req.prepare()
        response = self.session.send(
            prepared, 
            verify=True
        )
        
        if response.status_code != 200 or 'error' in response.headers:
            raise RuntimeError("Invalid username or password")
        else:
            self._account = response.json()
            self._token = self._account['tk']
            self._uniqueid = self._account['id']
           
            # all future session requests should contain our token, and 
            # (maybe?) some false Agent info in the Header
            self.session.headers.update({
                'tk': self._token,
                #'User-Agent': 'Vesync/1.71.02 (iPhone; iOS 11.2.2; Scale/2.00)'
            })
            
        self._devices = []


    """
    get list of all devices associated with this account
    """
    def get_devices(self):
        req = requests.Request(
            'POST',
            BASE_URL + "/loadMain",
            json=None,
            # below is a HACK headers workaround! 
            # because Session object is not sending correct headers after 
            # the first request in __init__ block.
            #
            # See: https://github.com/requests/requests/issues/4301
            #
            # Maybe I'm just doing something wrong with Session though? 
            headers=dict(self.session.headers)
        )
        prepared = req.prepare()
        response = self.session.send(
            prepared, 
            verify=True
        )
            
        self._devices = response.json()['devices']
        return self._devices


    def turn_on(self, id):
        return self.switch_outlet(id, 1)
        

    def turn_off(self, id):
        return self.switch_outlet(id, 0)
            
            
    """
    switch the outlet on or off:
    
    params:
        1. self
        2. id of the outlet/device
        3. state (0|1 (off|on))
    """
    def switch_outlet(self, oid, state):
        headers = dict(self.session.headers)
        headers.update({
            'id': self._uniqueid
        })
        data = {
            'cid': oid,
            'uri': '/relay',
            'action': 'break',
        }
        if state:
            data['action'] = 'open'
        
        req = requests.Request(
            'POST',
            BASE_URL + "/devRequest",
            json=data,
            headers=headers,
        )
        prepared = self.session.prepare_request(req)
        response = self.session.send(
            prepared, 
            verify=True,
        )
        
        if response.status_code != 200 or 'error' in response.headers:
            raise RuntimeError("Relay Switch Failure")
            
        return response.json()
             
        

