
~~~Overview~~~
The SGTPolicyCheck python package allows a user to do a live check on two authenticated hosts on an enterprise network 
to determine whether a Cisco TrustSec policy is restricting access between them.

The following logic is executed when the __main__.py script is run:
- Prompt the user for information about two hosts of interest
- Prompt the user for information about the ISE environment the script should query
- Checks the config for the appropriate settings specified by the user
- Resolves hostnames (if hostnames, not IP addresses, provided by user)
- Queries the ISE MNT API for session information using the IP Address of each host
- Parses the ISE session information to determine the tag value of each host
- Queries the ISE ERS API to idenitfy the TrustSec Matrix Cell which contains the policy for the idenitified tags
- Queries the ISE ERS API to idenitfy the TrustSec Matrix SGACLS contained in the identified cells
- Queries the ISE ERS API to idenitfy the specific content of SGACLS contained in the identified cells
- Summarizes the segmentation policy between the two hosts of interest


~~~Requirements~~~
The python version used to develop and test was python 3.9.6. It is recommended to use this version. Also,before using 
the package, be sure to install the packages specified in the requirements.txt file with the following command:

pip install [package]


~~~Package Use~~~
A user or front-end application makes use of the package by issuing following command:

python3 /[path]/SGTPolicyCheck --environment ['Dev'|'Test'|'Prod'] --host1 [hostname] --host2 [hostname] --apiusername [user] --apipassword [pass]
python3 /[path]/SGTPolicyCheck --environment ['Dev'|'Test'|'Prod'] --ipaddr1 [ipaddr] --ipaddr2 [ipaddr] --apiusername [user] --apipassword [pass]


~~ Host Inputs ~~
The user/application backend can provide any two host, either by hostname or ip address, using any combination of the below 
parameters: 

("-h1" or "--host1")("-h2" or "--host2")
("-i1" or "--ipaddr1")("-i2" or "--ipaddr2")

If given a hostname, the SGTPolicyCheck package will subsequently attempt to resolve the hostname to an IPaddress.
These client IP addresses will be used to make queries to the ISE ERS and ISE MNT REST APIs. 

If ipaddresses or tags cannot be determined for both hosts (ie. Not authenticated to ISE), the program will exit and
display an error.


~~ ISE inputs ~~
The user is required to provide the '--environment' parameter:

("-e" or "--environment")

 This parameter specifies which instances of ISE will be queried for Cisco TrustSec policy information. Each environment
 has ISE networking settings that can be configured in the config.py file.


~~ Credentials ~~
Credentials for the 'DEV' and 'TEST' environment have values that can be configured in the config.py file. Credentials for 
the 'PROD' environment must be passed as command-line arguments. This makes it very difficult to 'accidentally' kick off the 
script towards the production environment

To provide credentials as command-line arguments, the following parameters are available:

"-u" or "--apiusername" 
"-p" or "--apipassword"

The --apiusername and --apipassword arguments are the credentials that will be passed to ISE for HTTPBasic Authentication.
For the package to work, the credentials provided must have ERS Admin and MNT Admin permissions in the relevant ISE environment


~~ Example Use ~~
export $USERNAME = "ProdUser"
export $PASSWORD = "ProdPass"  
cd /src
source venv/bin/activate
python SGTPolicyCheck Prod $USERNAME $PASSWORD R123456.mayo.edu R654321.mayo.edu