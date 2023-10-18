import traceback
import requests
import config
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TrustSecMatrix:
    def __init__(self,environment):
        self.totalcells = int()
        self.matrixcells = []
        self.environment = environment
        self.envsettings = ""
        self.defaultrule = "Permit IP"
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

class TrustSecMatrixCell(TrustSecMatrix):
    def __init__(self,environment):
        super().__init__(environment)
        self.totalcells = 1
        self.cellId = None
        self.cellName = None
        self.emptycell = None
        self.egressMatrixCellDetails = {}
        self.SGACLIDs = []
        self.SGACLnames = []
        self.SGACLcontent = []
    
    def getMatrixCellInfo(self,SrcTagName,DstTagName,APIUsername,APIPassword):
        try:
            getmatrixcellIDurl = self.envsettings.ERS_BASE_URL + "/egressmatrixcell?filter=sgtSrcName.EQ." + SrcTagName + "&filter=sgtDstName.Eq." + DstTagName
            headers = {"Accept":"application/json","Content-Type":"application/json"}
            ISEAPICall = requests.get(getmatrixcellIDurl,auth=(APIUsername,APIPassword),headers=headers,verify=False)
            ISEAPICall.raise_for_status()
            APIResponseData = ISEAPICall.json()
            self.matrixcells = APIResponseData['SearchResult']['resources']
            self.totalcells = APIResponseData['SearchResult']['total']
            if APIResponseData['SearchResult']['total'] == 0:
                self.cellId = None
                self.SGACLIDs = None
                self.SGACLnames = None
                self.emptycell = True
                return self
            elif APIResponseData['SearchResult']['total'] == 1:
                self.cellId = APIResponseData['SearchResult']['resources'][0]['id']
                self.cellName = str(APIResponseData['SearchResult']['resources'][0]['name'])
                self.emptycell = False
                return self
            else:
                print("Unexpected Use Case - More than 1 ISE Matrix cell returned")
        except requests.exceptions.RequestException as httperror:
            print("ISE ERS API Call Failed")
            print(httperror)
            print(traceback.format_exc())
        except Exception as error:
            print(error)
            print(traceback.format_exc())

    def getCellSGACLIDs(self,APIUsername,APIPassword,cellid):
        try:
            getsgaclIDurl = str(self.envsettings.ERS_BASE_URL) + "/egressmatrixcell/" + str(cellid)
            headers = {"Accept":"application/json","Content-Type":"application/json"}
            ISEAPICall = requests.get(getsgaclIDurl,auth=(APIUsername,APIPassword),headers=headers,verify=False)
            ISEAPICall.raise_for_status()
            APIResponseData= ISEAPICall.json()
            self.egressMatrixCellDetails = APIResponseData['EgressMatrixCell']
            self.SGACLIDs = self.egressMatrixCellDetails['sgacls']
            return self
        except requests.exceptions.RequestException as httperror:
            print("ISE ERS API Call Failed")
            print(httperror)
            print(traceback.format_exc())
        except Exception as error:
            print(error)
            print(traceback.format_exc())
    
    def getSGACLbyID(self,APIUsername,APIPassword,SGACLIDs):
        try:
            i = len(self.SGACLIDs)
            for sgaclID in self.SGACLIDs:
                getSGACLdetailsurl = self.envsettings.ERS_BASE_URL + "/sgacl/" + sgaclID
                headers = {"Accept":"application/json","Content-Type":"application/json"}
                ISEAPICall = requests.get(getSGACLdetailsurl,auth=(APIUsername,APIPassword),headers=headers,verify=False)
                ISEAPICall.raise_for_status()
                APIResponseData= ISEAPICall.json()
                self.SGACLcontent.append(APIResponseData['Sgacl']['aclcontent'])
                self.SGACLnames.append(APIResponseData['Sgacl']['name'])
                if i > 1:
                    time.sleep(1)
                return self
        except requests.exceptions.RequestException as httperror:
            print("ISE ERS API Call Failed")
            print(httperror)
            print(traceback.format_exc())
        except Exception as error:
            print(error)
            print(traceback.format_exc())
    
    