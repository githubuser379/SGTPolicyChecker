import traceback
import authenticatedhost
import isematrix
import sys
import argparse
import config
import time
import socket

def main():    
    ### Define and parse arguments from 'python SGTPolicyCheck' shell command
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-e","--environment",help="Dev,Test, or Prod Environment",required=True)
        parser.add_argument("-u","--apiusername", help="Username for ISE API (via environment variable - $USERNAME)", required=False)
        parser.add_argument("-p","--apipassword", help="Password for ISE API (via environment variable - $PASSWORD)", required=False)
        parser.add_argument("-h1","--host1", help="Hostname of First Host", required=False)
        parser.add_argument("-h2","--host2", help="Hostname of Second Host", required=False)
        parser.add_argument("-i1","--ipaddr1",help="IP Address of First Host",required=False)
        parser.add_argument("-i2","--ipaddr2",help="IP Address of Second Host",required=False)
        args = parser.parse_args()
    except parser.error:
        error = sys.exc_info()[0]
        print(traceback.format_exc())
        print(error)
    
    ### Define global variables
    iseenvironment = "Dev,Test, or Prod placeholder variable"
    apiusername = "Username placeholder variable"
    apipassword = "Password placeholder variable"
    
    ### Assign variable values
    iseenvironment = args.environment
    apiusername = args.apiusername
    apipassword = args.apipassword

    ### Instantiate host objects
    """Placeholder object to hold info for Host1"""
    Host1 = authenticatedhost.AuthenticatedClient(iseenvironment)
    """Placeholder object to hold info for Host2"""
    Host2 = authenticatedhost.AuthenticatedClient(iseenvironment)

    ### Assign attributes to host objects
    Host1.hostname = args.host1
    Host2.hostname = args.host2
    Host1.ipaddress = args.ipaddr1
    Host2.ipaddress = args.ipaddr2

    ### Set environment configurations by referencing config.py file
    if iseenvironment == "Dev":
        DevEnvironmentInstance = config.DevEnvironmentSettings()
        apiusername = DevEnvironmentInstance.DevUser
        apipassword = DevEnvironmentInstance.DevPass
    elif iseenvironment == "Test":
        TestEnvironmentInstance = config.TestEnvironmentSettings()
        apiusername = TestEnvironmentInstance.TestUser
        apipassword = TestEnvironmentInstance.TestPass
    elif iseenvironment == "Prod":
        ProdEnvironmentInstance = config.ProdEnvironmentSettings()
    else:
        print("Please reiusse 'python3 SGTPolicyCheck' command with the value 'Dev','Test', or 'Prod' as the ISE environment argument")
        sys.exit()

    ### Resolve IP Address for hostnames provided as arguments (if IP addresses weren't given)
    print("\n~~ Resolving provided hostnames ~~")
    try:
        if Host1.ipaddress == None: 
            Host1.ipaddress = socket.gethostbyname(Host1.hostname)
            print("Host1 Hostname: " + Host1.hostname)
            print("Host1 IP: " + Host1.ipaddress)
        if Host2.ipaddress == None: 
            Host2.ipaddress = socket.gethostbyname(Host2.hostname)
            print("Host2 Hostname: " + Host2.hostname)
            print("Host2 IP: " + Host2.ipaddress)
    except Exception as error:
        print("Could not resolve hostnames")
        print(error)
        print(traceback.format_exc())
        sys.exit()
    
    ### Get authentication session information from ISE MNT node API (including tag value) for both hosts 
    try:
        print("\n~~ Retrieving authentication session information ~~") 
        ipaddress1 = Host1.ipaddress
        Host1.getclientauthsession(ipaddress1,apiusername,apipassword)
        print("Host1 Mac Address: " + Host1.macaddress)
        print("Host1 AuthzProfile: " + Host1.authzprofile)
        print("Host1 Tag: " + Host1.securitygrouptag)
    except Exception as error:
        print("Could not retrieve Host1 tag from ISE MNT node")
        print(error)
        print(traceback.format_exc())
        sys.exit()

    try:
        ipaddress2 = Host2.ipaddress
        Host2.getclientauthsession(ipaddress2,apiusername,apipassword)
        print("Host2 Mac Address: " + Host2.macaddress)
        print("Host2 AuthzProfile: " + Host2.authzprofile)
        print("Host2 Tag: " + Host2.securitygrouptag)
    except Exception as error:
        print("Could not retrieve Host2 tag from ISE MNT node")
        print(error)
        print(traceback.format_exc())
        sys.exit()

    ### Setup ISE Matrix Cell Objects to store information about the revelant cells retrieced from the ISE API
    isematrixcellobject1 = isematrix.TrustSecMatrixCell(iseenvironment)
    isematrixcellobject2 = isematrix.TrustSecMatrixCell(iseenvironment)

    ### Get ISE Matrix Cell IDs and attributes for retrieved host tags from ISE ERS API
    try:
        SrcTagtoDstTagCell = isematrixcellobject1.getMatrixCellInfo(Host1.securitygrouptag,Host2.securitygrouptag,apiusername,apipassword)
        print("\n~~ Host1->Host2 Cell info ~~")
        print(Host1.securitygrouptag + " -> " + Host2.securitygrouptag)
        print("SRC-DST Cell name: " + str(SrcTagtoDstTagCell.cellName))
        print("Cell ID: " + str(SrcTagtoDstTagCell.cellId))
        print("Is Empty Cell? " + str(SrcTagtoDstTagCell.emptycell))
        if SrcTagtoDstTagCell.emptycell == True:
            SrcTagtoDstTagCell.totalcells = 0
        else:
            pass
    except Exception as error:
        print("Could not retrieve cellID from ISE ERS API node for SRC->DST cell ")
        print(error)
        print(traceback.format_exc())
    try:
        DstTagtoSrcTagCell = isematrixcellobject2.getMatrixCellInfo(Host2.securitygrouptag,Host1.securitygrouptag,apiusername,apipassword)
        print("\n~~ Host2 -> Host1 Cell info ~~")
        print(Host2.securitygrouptag + " -> " + Host1.securitygrouptag)
        print("DST-SRC Cell name: " + str(DstTagtoSrcTagCell.cellName))
        print("Cell ID: " + str(DstTagtoSrcTagCell.cellId))
        print("Is Empty Cell? " + str(DstTagtoSrcTagCell.emptycell)+ "\n")    
        if DstTagtoSrcTagCell.emptycell == True:
                DstTagtoSrcTagCell.totalcells = 0
        else:
            pass
    except Exception as error:
        print("Could not retrieve cellID from ISE ERS API node for DST->SRC cell")
        print(error)
        print(traceback.format_exc())

    ### Get SGACL IDs for SGACLs configured in identified TrustSec Matrix Cells
    try:
        print("~~ Get SGACLids for SGACLS configured in identified TrustSec Matrix Cells ~~")
        if SrcTagtoDstTagCell.totalcells == 0:
            print(Host1.securitygrouptag + " -> " + Host2.securitygrouptag)
            print("Cell ID: " + str(SrcTagtoDstTagCell.cellId))
            print("No SGACLs are configured at cell intersection of " + Host1.securitygrouptag + "->" + Host2.securitygrouptag)
            print("No SGACL IDs to retrieve. Default matrix policy will apply \n")        
        else:
            SrcTagtoDstTagCell.getCellSGACLIDs(apiusername,apipassword,SrcTagtoDstTagCell.cellId)
            print(Host1.securitygrouptag + " -> " + Host2.securitygrouptag)
            print("Cell ID: " + str(SrcTagtoDstTagCell.cellId))
            print("SGACL ID List: " + str(SrcTagtoDstTagCell.SGACLIDs) + "\n")
    except Exception as error:
        print("Could not retrieve SRC->DST SGACL IDs from ISE ERS API") 
        print(error)
        print(traceback.format_exc())
    try:
        if DstTagtoSrcTagCell.totalcells == 0:
            print(Host2.securitygrouptag + " -> " + Host1.securitygrouptag)
            print("No SGACLs are configured at cell intersection of " + Host2.securitygrouptag + "->" + Host1.securitygrouptag)
            print("No SGACL IDs to retrieve. Default matrix policy will apply \n")
        else:
            DstTagtoSrcTagCell.getCellSGACLIDs(apiusername,apipassword,DstTagtoSrcTagCell.cellId)
            print(Host2.securitygrouptag + " -> " + Host1.securitygrouptag)
            print("Cell ID: " + str(DstTagtoSrcTagCell.cellId))
            print("SGACL ID List: " + str(SrcTagtoDstTagCell.SGACLIDs) + "\n")
    except Exception as error:
        print("Could not retrieve DST->SRC SGACL IDs from ISE ERS API")
        print(error)
        print(traceback.format_exc())
    
    ### Get SGACL Details by SGACL ID
    try:
        if SrcTagtoDstTagCell.SGACLIDs == None:
            pass
        else:
            SrcTagtoDstTagCell = SrcTagtoDstTagCell.getSGACLbyID(apiusername,apipassword,SrcTagtoDstTagCell.SGACLIDs)
    except Exception as error:
        print("Could not retrieve SRC->DST SGACL content details from ISE ERS API")
        print(error)
        print(traceback.format_exc())

    try:
        if DstTagtoSrcTagCell.SGACLIDs == None:
            pass
        else:
            DstTagtoSrcTagCell = DstTagtoSrcTagCell.getSGACLbyID(apiusername,apipassword,DstTagtoSrcTagCell.SGACLIDs)
    except Exception as error:
        print("Could not retrieve DST->SRC SGACL content details from ISE ERS API")
        print(error)
        print(traceback.format_exc())


    ### Summarize the SGT Policy between hosts
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
    print("~~~~~~~~~~~~~~~~~~ Segmentation Policy Results ~~~~~~~~~~~~~~~~~~ \n")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
    
    print("The following segmentation policy is in place for Host1 -> Host2:\n")
    if SrcTagtoDstTagCell.SGACLnames == None:
        print("Hostname1: " + str(Host1.hostname) + " -> " + "Hostname2: " + str(Host2.hostname))
        print(str(Host1.ipaddress) + " -> " + str(Host2.ipaddress))
        print(Host1.securitygrouptag + " -> " + Host2.securitygrouptag)
        print("Host1 NAC Authz Policy: " + Host1.authzprofile)
        print("Host2 NAC Authz Policy: " + Host2.authzprofile)
        print("Host1 Tag: " + Host1.securitygrouptag)
        print("Host2 Tag: " + Host2.securitygrouptag)
        print("Is Empty Cell? " + str(SrcTagtoDstTagCell.emptycell) + "\n")
        print("     " + str(SrcTagtoDstTagCell.matrixdefaultrule) + " (Default Policy)\n")
    else:
        print("Hostname1: " + str(Host1.hostname) + " -> " + "Hostname2: " + str(Host2.hostname))
        print(str(Host1.ipaddress) + " -> " + str(Host2.ipaddress))
        print(Host1.securitygrouptag + " -> " + Host2.securitygrouptag)
        for SGACLname in SrcTagtoDstTagCell.SGACLnames:
            print("Host1 NAC Authz Policy: " + Host1.authzprofile)
            print("Host2 NAC Authz Policy: " + Host2.authzprofile)
            print("Host1 Tag: " + Host1.securitygrouptag)
            print("Host2 Tag: " + Host2.securitygrouptag)
            
            print("SGACL name: " + str(SGACLname))
            print("SGACL content: \n")
            ACENumber = 1
            for AccessControlEntry in SrcTagtoDstTagCell.SGACLcontent:
                print("    " + str(ACENumber) + "  |  " + str(AccessControlEntry))
                ACENumber += 1
            print("\n")
    
    print("The following segmentation policy is in place for Host2 -> Host1:\n")
    if DstTagtoSrcTagCell.SGACLnames == None:
        print("Hostname2: " + str(Host2.hostname) + " -> " + "Hostname1: " + str(Host1.hostname))
        print(str(Host2.ipaddress) + " -> " + str(Host1.ipaddress))
        print(Host2.securitygrouptag + " -> " + Host1.securitygrouptag)
        print("Host2 NAC Authz Policy: " + Host2.authzprofile)
        print("Host1 NAC Authz Policy: " + Host1.authzprofile)
        print("Host2 Tag: " + Host2.securitygrouptag)
        print("Host1 Tag: " + Host1.securitygrouptag)
        print("Is Empty Cell? " + str(DstTagtoSrcTagCell.emptycell) + "\n") 
        print("     " + str(DstTagtoSrcTagCell.matrixdefaultrule) + " (Default Policy)\n")
    else:
        print("Hostname2: " + str(Host2.hostname) + " -> " + "Hostname1: " + str(Host1.hostname))
        print(str(Host2.ipaddress) + " -> " + str(Host1.ipaddress))
        print(Host2.securitygrouptag + " -> " + Host1.securitygrouptag)
        for SGACLname in DstTagtoSrcTagCell.SGACLnames:
            print("Host2 NAC Authz Policy: " + Host2.authzprofile)
            print("Host1 NAC Authz Policy: " + Host1.authzprofile)
            print("Host2 Tag: " + Host2.securitygrouptag)
            print("Host1 Tag: " + Host1.securitygrouptag)
            print("SGACL name: " +str(SGACLname))
            print("SGACL content: \n")
            ACENumber = 1
            for AccessControlEntry in DstTagtoSrcTagCell.SGACLcontent:
                print("    " + str(ACENumber) + "  |  " + str(AccessControlEntry))
                ACENumber += 1
            print('\n')

if __name__ == '__main__':
    main()