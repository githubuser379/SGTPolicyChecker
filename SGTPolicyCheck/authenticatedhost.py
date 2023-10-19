import traceback
import requests
import config
import xmltodict
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class AuthenticatedClient:
    def __init__(self,environment):
        self.hostname = None
        self.ipaddress = None
        self.macaddress = None
        self.securitygrouptag = None
        self.authzprofile = None
        self.environment = environment
        self.envsettings = ""
        self.setAPIconfig()

    def setAPIconfig(self):
        if self.environment == "Dev":
            DevEnv = config.DevEnvironmentSettings()
            self.envsettings = DevEnv
        elif self.environment== "Test": 
            TestEnv = config.TestEnvironmentSettings()
            self.envsettings = TestEnv
        elif self.environment == "Prod":
            ProdEnv = config.ProdEnvironmentSettings()
            self.envsettings = ProdEnv

    def getclientauthsession(self,IPAddress,APIUsername,APIPassword):        
        try:
            getauthsessionurl = self.envsettings.MNT_BASE_URL + "/Session/EndPointIPAddress/" + IPAddress
            responsecontenttype = "Accept:application/xml"
            ISEAPICall = requests.get(getauthsessionurl,auth=(APIUsername,APIPassword),verify=False)
            ISEAPICall.raise_for_status()
            APIResponseData = dict(xmltodict.parse(ISEAPICall.content))
            self.ipaddress = APIResponseData["sessionParameters"]["framed_ip_address"]
            self.macaddress = APIResponseData["sessionParameters"]["calling_station_id"]
            self.securitygrouptag = APIResponseData["sessionParameters"]["cts_security_group"]
            self.authzprofile = APIResponseData["sessionParameters"]["selected_azn_profiles"]
            return self
        except requests.exceptions.RequestException as httperror:
            print("ISE MNT API Call Failed")
            print(httperror)
            print(traceback.format_exc())
        except Exception as error:
            print(error)
            print(traceback.format_exc())
