class Thermostat_Data(object):
    def __init__(self, authData, home=None):

        self.getAuthToken = authData.access_token
        print("Token: ", self.getAuthToken)
        token_headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.getAuthToken}"
        }

        try:
            # print ("URL: ", _GETHOMEDATA_REQ)
            resp = requests.get(_GETHOMEDATA_REQ, headers=token_headers)
            if resp.status_code not in range(199, 300):
                print("Not in range: ", resp.status_code)  # resp.json(),
                raise Exception
        except Exception as err:
            print("code=%s, reason=%s" % (err.code, err.reason))
            return None

        # print(resp)
        odpoved = {}
        odpoved = resp.json()

        raw_homes = {}
        raw_homes = dict(enumerate(odpoved.get('body', {}).get('homes')))

        print(raw_homes)
        self.rawData = {}
        self.rawData = raw_homes
        # self.homes = { d['home_name'] : d["station_name"] for d in self.rawData }
        if not self.rawData:
            print("No hoome available")
            return

        # Setting selected home to self.homeData
        self.homeData = filter_home_data(self.rawData)

        if not self.homeData:
            print("No home %s found" % home)
            return

        # Selecting thermostates
        try:
            # print("Meno domu", self.homeData['name'])
            # self.homeData['name'] = self.homeData['name']
            m = {}
            m = dict(enumerate(self.homeData.get('modules', {})))
            self.defaultThermostat = m[1]
            # self.defaultThermostatId = self.homeData['id']
            # self.defaultModule = self.homeData['modules'][0]
        except Exception as e:
            # print("Status Code", resp.status_code)     #resp.json(),
            print("Error 3: ", e)

        return

    def moduleNamesList(self, home=None, type=None):
        if not home:
            home = self.homeData

        my_lst = list()
        if my_lst is not None:
            print('variable is NOT None')
            # my_list.append('hello')
        else:
            print('variable is None')

        print("list je: ", my_lst)

        for m in home['modules']:
            if not type:
            # l.append(m['name'])
            else:
                if home['type'] == type:
            # l.append(m['name'])
        print("Zoznam modulov: ", l)
        return l

    def toStr(self, thermName=None, home=None):
        res = [m['module_name'] for m in self.modules.values()]
        res.append(self.stationByName(station)['module_name'])
        return res

    def getThermostat(self, name=None, tid=None):
        if ['name'] != name:
            return None
        else:
            return
        return self.thermostat[self.defaultThermostatId]

    def getModuleByName(self, name, thermostatId=None):
        thermostat = self.getThermostat(tid=thermostatId)
        for m in thermostat['modules']:
            if m['name'] == name: return m
        return None

    def valveByName(self, valve=None):
        if not valve: valve = self.defaultThermostatId
        for i, s in self.stations.items():
            if s['station_name'] == station:
                return self.stations[i]
        return None

    def postRequest(self, hdrs=None):
        try:
            # print ("URL: ", _GETHOMEDATA_REQ)
            resp = requests.get(_GETHOMEDATA_REQ, headers=hdrs)
            if resp.status_code not in range(199, 300):
                print("Not in range: ", resp.status_code)  # resp.json(),
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
            if mod['module_name'] == module:
                return mod
        return None

    def moduleById(self, mid):
        return self.modules.get(mid)