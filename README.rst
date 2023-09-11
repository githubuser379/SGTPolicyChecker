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

~~ Installation ~~
Install python 3.9.6 and add python to the system path:

    *Windows
    My Computer > Properties > Advanced System Settings > Environment Variables >
    Just add the path as C:\[Install_Path]\Python3.9.6 (or wherever you installed python)

        OR

    Just select "Add Python to environment variables" during Wizard-based installation of Python

Manually download SGTPolicyCheck package from https://github.com/githubuser379/SGTPolicyChecker and install it on your 
computer wherever you'd like.

If git is installed on your computer, you can alternatively clone the repo from 
git@github.com:githubuser379/SGTPolicyChecker.git:

User1@R123456 ~ % pwd
/Users/User1
User1@R123456 ~ % mkdir PycharmProjects
User1@R123456 ~ % ls
PycharmProjects         
User1@R123456 ~ % cd PycharmProjects
User1@R123456 PycharmProjects % init git
User1@R123456 PycharmProjects % git clone git@github.com:githubuser379/SGTPolicyChecker.git
User1@R123456 PycharmProjects % ls
ISEAPI
User1@R123456 ~ % cd ISEAPI
User1@R123456 ISEAPI % cd src
User1@R123456 src % ls
README.rst              SGTPolicyCheck          requirements.txt


~~~Requirements~~~
The python version used to develop and test was python 3.9.6. It is recommended to use this version. Also,before using 
the package, be sure to install the packages specified in the requirements.txt file with the following terminal command:

pip install -r requirements.txt

    OR

pip install [individual_package_1]
pip install [individual_package_2]
    ...
pip install [individual_package_n]

'pip' comes by default with python, but if for some reason it needs to be reinstalled, instruction can be found here:
https://pip.pypa.io/en/stable/installation/

You can also try re-installing python 3.9.6.

~~~Package Use~~~
A user or front-end application makes use of the package by issuing some variation of the following command:

python3 /[install_path]/SGTPolicyCheck --environment ['Dev'|'Test'|'Prod'] --host1 [hostname] --host2 [hostname] --apiusername [user] --apipassword [pass]
python3 /[install_path]/SGTPolicyCheck --environment ['Dev'|'Test'|'Prod'] --ipaddr1 [ipaddr] --ipaddr2 [ipaddr] --apiusername [user] --apipassword [pass]
python3 /[install_path]/SGTPolicyCheck --environment ['Dev'|'Test'|'Prod'] --host1 [hostname] --ipaddr1 [ipaddr] --apiusername [user] --apipassword [pass]
python3 /[install_path]/SGTPolicyCheck --environment ['Dev'|'Test'|'Prod'] --ipaddr1 [ipaddr] --host1 [hostname] --apiusername [user] --apipassword [pass]

~~ Host Inputs ~~
The user/application backend can provide any two hosts, either by hostname or ip address, using any combination of the below 
parameters: 

("-h1" or "--host1")("-h2" or "--host2")
("-i1" or "--ipaddr1")("-i2" or "--ipaddr2")

If given a hostname, the SGTPolicyCheck package will attempt to resolve the hostname to an IPaddress. These client IP 
addresses will be used to make queries to the ISE MNT REST APIs to retrieve authentication session information. 

If the IP addresses or tags cannot be determined for both hosts (ie. Not authenticated to ISE), the program will exit and
display an error.


~~ ISE inputs ~~
The user/application is required to provide the '--environment' parameter:

("-e" or "--environment")

This parameter specifies which instances of ISE will be queried for Cisco TrustSec policy information. Each ISE environment 
has network configuration settings that can be configured in the config.py file.


~~ Credentials ~~
Credentials for the 'DEV' and 'TEST' environment have values that can be configured in the config.py file. Credentials for 
the 'PROD' environment must be passed as command-line arguments. This makes it more difficult to 'accidentally' kick off the 
script towards the production environment.

To provide credentials as command-line arguments, the following parameters are available:

"-u" or "--apiusername" 
"-p" or "--apipassword"

The --apiusername and --apipassword arguments are the credentials that will be passed to the ISE API for HTTPBasic 
Authentication. For the package to work, the credentials provided must have ERS Admin and MNT Admin permissions in the 
relevant ISE environment


~~ Example Use ~~
export $USERNAME = "ProdUser"
export $PASSWORD = "ProdPass"  
cd /[install_path]
source venv/bin/activate
python /src/SGTPolicyCheck Prod -u $USERNAME -p $PASSWORD -h1 R123456.mayo.edu -h2 R654321.mayo.edu
 
cd /[install_path]
source venv/bin/activate
python /src/SGTPolicyCheck Dev -h1 R123456.mayo.edu -h2 R654321.mayo.edu

cd /[install_path]
source venv/bin/activate
python /src/SGTPolicyCheck Dev -i1 10.249.37.229 -i2 10.249.21.40