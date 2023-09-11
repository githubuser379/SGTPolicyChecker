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
        self.cellID = None
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
                pass
            elif APIResponseData['SearchResult']['total'] == 1:
                self.cellId = APIResponseData['SearchResult']['resources'][0]['id']
                self.cellName = str(APIResponseData['SearchResult']['resources'][0]['name'])
                self.emptycell = False
                print("CellID: " + self.cellID)
                print("CellName: " + self.cellName)
            else:
                print("Unexpected Use Case - More than 1 ISE Matrix cell returned")
            return self
        except requests.exceptions.RequestException as httperror:
            print("ISE ERS API Call Failed")
            print(httperror)
        except Exception as error:
            print(error)

    def getCellSGACLIDs(self,APIUsername,APIPassword):
        try:
            getsgaclIDurl = self.envsettings.ERS_BASE_URL + "/egressmatrixcell/" + self.cellID
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
        except Exception as error:
            print(error)
    
    def getSGACLbyID(self,APIUsername,APIPassword):
        try:
            i = len(self.SGACLIDs)
            for sgaclID in self.SGACLIDs:
                getSGACLdetailsurl = self.envsettings.ERS_BASE_URL + "/sgacl/" + sgaclID
                headers = {"Accept":"application/json","Content-Type":"application/json"}
                ISEAPICall = requests.get(getSGACLdetailsurl,auth=(APIUsername,APIPassword),headers=headers,verify=False)
                ISEAPICall.raise_for_status()
                APIResponseData= ISEAPICall.json()
                self.SGACLcontent.append(APIResponseData['sgacl']['aclcontent'])
                self.SGACLnames.append(APIResponseData['sgacl']['name'])
                if i > 1:
                    time.sleep(1)
            return self
        except requests.exceptions.RequestException as httperror:
            print("ISE ERS API Call Failed")
            print(httperror)
        except Exception as error:
            print(error)
    
    