
from _kluce import *
import requests, datetime
import pandas as pd
import json

# 2 : Override hard coded values with credentials file if any

_CLIENT_ID     = client_id
_CLIENT_SECRET = secret_id
_USERNAME      = login_net
_PASSWORD      = passw_net

#########################################################################


# Common definitions

_BASE_URL = "https://api.netatmo.com/"
_AUTH_REQ              = _BASE_URL + "oauth2/token"
_GETMEASURE_REQ        = _BASE_URL + "api/getmeasure"
_GETSTATIONDATA_REQ    = _BASE_URL + "api/getstationsdata"
_GETTHERMOSTATDATA_REQ = _BASE_URL + "api/getthermostatsdata"
_GETHOMEDATA_REQ       = _BASE_URL + "api/homesdata"
_GETCAMERAPICTURE_REQ  = _BASE_URL + "api/getcamerapicture"
_GETEVENTSUNTIL_REQ    = _BASE_URL + "api/geteventsuntil"


_POST_UPDATE_HOME_REQ  = _BASE_URL + "/api/updatehome"

# UNITS used by Netatmo services
UNITS = {
    "unit" : {
        0: "metric",
        1: "imperial"
    },
    "windunit" : {
        0: "kph",
        1: "mph",
        2: "ms",
        3: "beaufort",
        4: "knot"
    },
    "pressureunit" : {
        0: "mbar",
        1: "inHg",
        2: "mmHg"
    },
    "thermunit": {
        0: "celsius",
        1: "farenheit"
    }
}

class NetatmoAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    refresh_token = None
    client_id = None
    secret_id = None
    login_net = None
    passw_net = None
    token_url = _AUTH_REQ
    
    def __init__(self, client_id, secret_id, login_net, passw_net, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.secret_id = secret_id
        self.login_net = login_net
        self.passw_net = passw_net
    
    def get_client_credentials(self):
        client_id = self.client_id
        client_secret = self.secret_id
        login_net = self.login_net
        passw_net = self.passw_net
        if secret_id == None or client_id == None or login_net == None or passw_net == None:
            raise Exception("You must set client_id and Client_secret!")
        return {
            "client_id": client_id,
            "client_secret": secret_id,
            "username": login_net,
            "password": passw_net,
        }
    
    def get_token_headers(self):
        return {
            "Host": "api.netatmo.com",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        }
    
    def get_token_data(self):
        partial_token_data = {
            "grant_type": "password",
            "scope": "read_thermostat write_thermostat"
        }
        #final_token_dada = self.Merge (self.get_client_credentials(), partial_token_data)
        final_token_dada = partial_token_data | self.get_client_credentials()
        return final_token_dada
        
        
    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        print (token_data)
        token_headers = self.get_token_headers()
        
        r = requests.post(token_url, data=token_data, headers = token_headers)
        print (r.json())
        print (r)

        if r.status_code not in range(200, 299):
            return False
        
        data = r.json()
        
        now = datetime.datetime.now()
        access_token = data['access_token']
        refresh_token = data['refresh_token']
        expires_in = data['expires_in']               # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now    
        return True
    
    def get_auth_data(self):
        clientAuth = {"access_token": self.access_token,
            "access_token_expires": self.access_token_expires,
            "access_token_did_expire": self.access_token_did_expire,
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "secret_id": self.secret_id,
            "login_net": self.login_net,
            "passw_net": self.passw_net,
            "token_url": self.token_url
        }
        
        return clientAuth

client = NetatmoAPI(client_id, secret_id, login_net, passw_net)

client.perform_auth()


client.access_token_expires


client.access_token


client.refresh_token


client.get_auth_data()

def info(token):
    token_headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {token}"
        }
    
    token_url = _GETHOMEDATA_REQ
    token_data = {
        "access_token" : token
    }
    print (token_data['access_token'])
    
    r = requests.get("https://api.netatmo.com/api/homesdata", headers = token_headers)

    print (r.json())
    print (r)

    if r.status_code not in range(200, 299):
        print ("False")
        return False
        
    data = r.json()
    print("True")
    return True

info(client.access_token)

class Thermostat_Data(object):
    raw_homes = []                  # údaje o všetkých doomoch
    rawData = {}                    # údaje o vybranom dome
    
    def __init__(self, authData, home=None):

        self.getAuthToken = authData.access_token
        print("Token: ", self.getAuthToken)
        token_headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.getAuthToken}"
        }
        
        try:
            #print ("URL: ", _GETHOMEDATA_REQ)
            resp = requests.get(_GETHOMEDATA_REQ, headers = token_headers)
            if resp.status_code not in range(199, 300):
                print("Not in range: ", resp.status_code) #resp.json(),
                raise Exception
        except Exception as err:
            print("code=%s, reason=%s" % (err.code, err.reason))
            return None
        
        # JSON objekt, v ktorom sú údaje o dome
        # get/homestatus
        odpoved = resp.json()
        
        # Načitanie json do suboru pre kontrolu
        #jsonString = json.dumps(odpoved)
        #jsonFile = open("data.json", "w")
        #jsonFile.write(jsonString)
        #jsonFile.close()
        
        
        # obsahuje základné informácie o dome a štruktúre zariadení a tiež o užívateľovi, status a ...
        # načítanie zoznamu domov = list of sets and lists
        raw_homes = dict(enumerate(odpoved.get('body', {}).get('homes')))
        
        #print (raw_homes)
        
        # Načítanie zoznamu domov do dict rawData
        self.rawData = raw_homes
        
        if not self.rawData :
            print("Nie je žiaden dom")
            return
        
        # Načítanie vybratéhoo domu do dict: self.homeData
        #print(type(raw_homes))
        idhome = "59d3da1c7a7570a21d8c1575"
        self.homeData = self.filter_home_data(self.rawData, idhome)
        
        if not self.homeData: 
            print("No home %s found" % home)
            return
        
        # Selecting thermostates
        try: 
            #print("Meno domu", self.homeData['name'])
            m = {}
            m = dict(enumerate(self.homeData.get('modules', {})))
            self.defaultThermostat = m[1]
            #self.defaultThermostatId = self.homeData['id']
            #self.defaultModule = self.homeData['modules'][0]
        except Exception as e:
            #print("Status Code", resp.status_code)     #resp.json(), 
            print("Error 3: ", e)
        
        return

    def moduleNamesList(self, home=None, type=None):
        if not home:
            home = self.homeData
        
        my_lst = list()
        if my_lst is not None:
            print('variable is NOT None')
            #my_list.append('hello')
        else:
            print('variable is None')
            
        print ("list je: ", my_lst)
        
        for m in home['modules']:
            if not type:
                my_lst.append(m['name'])
            else:
                if home['type'] == type:
                    my_lst.append(m['name'])
        print ("Zoznam modulov: ", my_lst)
        return my_lst
    
    def filter_home_data(self, Domy, home=None):
        # Find a home who's home id or name is the one requested
        for h in Domy:
            if Domy[h]["name"] == home or Domy[h]["id"] == home:
                #print ("filter_home_data: vychádzam z druhej slučky", rawData[h]["name"])
                return Domy[h]
        return None

    def toStr(self, thermName=None, home=None):
        res = [m['module_name'] for m in self.modules.values()]
        res.append(self.stationByName(station)['module_name'])
        return res
    
    def getThermostat(self, name=None, tid=None):
        if ['name'] != name: return None
        else: return 
        return self.thermostat[self.defaultThermostatId]


    def getModuleByName(self, name, thermostatId=None):
        thermostat = self.getThermostat(tid=thermostatId)
        for m in thermostat['modules']:
            if m['name'] == name: return m
        return None
    
    def valveByName(self, valve=None):
        if not valve : valve = self.defaultThermostatId
        for i,s in self.stations.items():
            if s['station_name'] == station :
                return self.stations[i]
        return None

    def postRequest(self, hdrs=None):
        try:
            #print ("URL: ", _GETHOMEDATA_REQ)
            resp = requests.get(_GETHOMEDATA_REQ, headers = hdrs)
            if resp.status_code not in range(199, 300):
                print("Not in range: ", resp.status_code) #resp.json(),
                raise Exception
        except Exception as err:
            print("code=%s, reason=%s" % (err.code, err.reason))
            return None
        
        return resp.json()




    # Meteo
    def modulesNamesList(self, thermName=None, home=None):
        res = [m['module_name'] for m in self.modules.values()]
        res.append(self.stationByName(station)['module_name'])
        return res



    def stationById(self, sid):
        return self.stations.get(sid)

    def moduleByName(self, module):
        for m in self.modules:
            mod = self.modules[m]
            if mod['module_name'] == module :
                return mod
        return None

    def moduleById(self, mid):
        return self.modules.get(mid)

therm = Thermostat_Data(client)
print (therm.moduleNamesList())
