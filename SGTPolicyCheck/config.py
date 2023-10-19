class RuntimeSettings:
    def __init__(self): 
        self.ENV_NAME = "'Prod','Test' or 'Dev'"
        self.ERS_HOST = "PAN_IP_Address"
        self.MNT_HOST = "MNT_IP_Address"
        self.ERS_PORT = "ERS API Port Number"
        self.MNT_PORT = "MNT API Port Number"
        self.ERS_BASE_URL = "Full ERS API URL"
        self.MNT_BASE_URL = "Full MNT API URL"
        
class DevEnvironmentSettings(RuntimeSettings):
    def __init__(self):
        super().__init__()
        self.ENV_NAME ="Dev"
        self.ERS_HOST = "rooc01lac01.mayo.edu"
        self.MNT_HOST = "rooc01lac02.mayo.edu"
        self.ERS_PORT = "9060"
        self.MNT_PORT = "443"
        self.ERS_BASE_URL = "https://" + self.ERS_HOST + ":" + self.ERS_PORT + "/ers/config"
        self.MNT_BASE_URL = "https://" + self.MNT_HOST + ":" + self.MNT_PORT + "/ise/mnt/api"
        self.DevUser = "DevUser"
        self.DevPass = "DevPass"
        # Example cmd session:
        #   cd /src
        #   python SGTPolicyCheck -e Dev -u DevUser -p TestPass -h1 R123456.mayo.edu -h2 R654321.mayo.edu
    
class TestEnvironmentSettings(RuntimeSettings):
    def __init__(self):
        super().__init__()
        self.ENV_NAME ="Test"
        self.ERS_HOST = "rooc01lac04.mayo.edu"
        self.MNT_HOST = "rooc01lac05.mayo.edu"
        self.ERS_PORT = "9060"
        self.MNT_PORT = "443"
        self.ERS_BASE_URL = "https://" + self.ERS_HOST + ":" + self.ERS_PORT + "/ers/config"
        self.MNT_BASE_URL = "https://" + self.MNT_HOST + ":" + self.MNT_PORT + "/ise/mnt/api"
        self.TestUser = "TestUser"
        self.TestPass = "TestPass"
        # Example cmd session:
        #   cd /src
        #   python SGTPolicyCheck -e Test -u TestUser -p TestPass -h1 R123456.mayo.edu -h2 R654321.mayo.edu

class ProdEnvironmentSettings(RuntimeSettings):
    def __init__(self):
        super().__init__()
        self.ENV_NAME ="Prod"
        self.ERS_HOST = "Test in Lab First"
        self.MNT_HOST = "Test in Lab First"
        self.ERS_PORT = "9060"
        self.MNT_PORT = "443"
        self.ERS_BASE_URL = "https://" + self.ERS_HOST + ":" + self.ERS_PORT + "/ers/config"
        self.MNT_BASE_URL = "https://" + self.MNT_HOST + ":" + self.MNT_PORT + "/ise/mnt/api"
        # "DONT ADD PROD CREDENTIALS TO CODE OR TYPE IN PLAINTEXT!!!"
        # "Use Environment Variables for Production Environment when executing script"
        # Example cmd session:
        #   export $USERNAME = "ProdUser"
        #   export $PASSWORD = "ProdPass"  
        #   cd /src
        #   python SGTPolicyCheck -e Prod -u $USERNAME -p $PASSWORD -h1 R123456.mayo.edu -h2 R654321.mayo.edu