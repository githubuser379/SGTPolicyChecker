~~~~~~~~~~~~~~~~
~~~ Overview ~~~
~~~~~~~~~~~~~~~~

The SGTPolicyCheck python package allows a user to do a live check on two authenticated hosts on an enterprise network 
to determine whether a Cisco TrustSec policy is restricting access between them.

The following logic is executed when the __main__.py script is run:

- Parses user provided information about two hosts of interest

- Parses user provided information about the ISE environment the script should query

- Checks and intializes the config settings for the environment specified by the user

- Resolves hostnames (if hostnames, not IP addresses, provided by user)

- Queries the ISE MNT API for session information using the IP Address of each host

- Parses the ISE MNT API session information to determine the tag value of each host

- Queries the ISE ERS API to idenitfy the TrustSec Matrix Cell which contains the policy for the idenitified tags

- Queries the ISE ERS API to idenitfy the TrustSec Matrix SGACLS contained in the identified cells

- Queries the ISE ERS API to idenitfy the specific content of SGACLS contained in the identified cells

- Summarizes the segmentation policy between the two hosts of interest


~~~~~~~~~~~~~~~~~~
~~ Installation ~~
~~~~~~~~~~~~~~~~~~

Install python 3.9.6 and add python to the system path:

    *Windows
    My Computer > Properties > Advanced System Settings > Environment Variables >
    Just add the path as C:\[Install_Path]\Python3.9.6 (or wherever you installed python)

        OR

    Just select "Add Python to environment variables" during Wizard-based installation of Python

Manually download SGTPolicyCheck package from https://github.com/githubuser379/SGTPolicyChecker and place the folder 
wherever you'd like on your computer.

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


~~~~~~~~~~~~~~~~~~~~
~~~ Requirements ~~~
~~~~~~~~~~~~~~~~~~~~

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

~~~~~~~~~~~~~~~~~~~
~~~ Package Use ~~~
~~~~~~~~~~~~~~~~~~~

A user or front-end application makes use of the package by issuing some variation of the following command:

python3 /[install_path]/SGTPolicyCheck --environment ['Dev'|'Test'|'Prod'] --hostname1 [hostname] --hostname2 [hostname] --apiusername [user] --apipassword [pass]

python3 /[install_path]/SGTPolicyCheck --environment ['Dev'|'Test'|'Prod'] --ipaddress1 [ipaddress] --ipaddress2 [ipaddress] --apiusername [user] --apipassword [pass]

python3 /[install_path]/SGTPolicyCheck --environment ['Dev'|'Test'|'Prod'] --hostname1 [hostname] --ipaddress1 [ipaddr] --apiusername [user] --apipassword [pass]

python3 /[install_path]/SGTPolicyCheck --environment ['Dev'|'Test'|'Prod'] --ipaddress1 [ipaddr] --host1 [hostname] --apiusername [user] --apipassword [pass]

~~~~~~~~~~~~~~~~~~~
~~~ Host Inputs ~~~
~~~~~~~~~~~~~~~~~~~

The user/application backend can provide any two hosts, either by hostname or ip address, using any combination of the below 
parameters: 

("-h1" or "--host1")("-h2" or "--host2")

("-i1" or "--ipaddr1")("-i2" or "--ipaddr2")

If given a hostname, the SGTPolicyCheck package will attempt to resolve the hostname to an IPaddress. These client IP 
addresses will be used to make queries to the ISE MNT REST APIs to retrieve authentication session information. 

If the IP addresses or tags cannot be determined for both hosts (ie. Not authenticated to ISE), the program will exit and
display an error. If IP addresses and tags can be determined, the remaining API queries will continue and whatever policy
information can be retrieved from subsequent API calls will still be displayed to the user.

~~~~~~~~~~~~~~~~~~
~~~ ISE inputs ~~~
~~~~~~~~~~~~~~~~~~

The user/application is required to provide the '--environment' parameter:

("-e" or "--environment")

This parameter specifies which instances of ISE will be queried for Cisco TrustSec policy information. Each ISE environment 
has network configuration settings that can be configured in the config.py file.

If a non-acceptable value is provided by the user (not 'Dev','Test',or 'Prod') the program will remind the user of the
acceptable values and the program will then exit.

~~~~~~~~~~~~~~~~
~~~ ISE APIs ~~~
~~~~~~~~~~~~~~~~

This package calls the ISE MNT API to retrieve the following information for each endpoint:

- Mac Address

- ISE Authorization Profile

- Cisco TrustSec Security Group Tag

This package calls the ISE ERS API to retrieve the following information:

- Relevant TrustSec Matrix Cell ID

- Relevant SGACL IDs

- Relevant SGACL content

The ISE MNT API documentation can be found here: 
https://developer.cisco.com/docs/identity-services-engine/3.0/#!using-api-calls-for-session-management/detailed-session-attribute-api-calls


The ISE ERS API documentation can be found here:
https://developer.cisco.com/docs/identity-services-engine/3.0/#!cisco-ise-api-documentation


~~~~~~~~~~~~~~~~~~~~~~~~~
~~~ ISE MNT API Call ~~~
~~~~~~~~~~~~~~~~~~~~~~~~~

The ISE MNT API calls used by this package include the following:
- https://<ise_mnt_node>:443/ise/mnt/api/Session/EndPointIPAddress/<endpoint_ip>

The ISE MNT node provides an HTTP response with a HTTP body that includes authentication session attributes wrapped inside
 an element called 'sessionParameters':

    <sessionParameters>

      <passed xsi:type="xs:boolean">true</passed>

      <calling_station_id>00:0C:29:95:A5:C1</calling_station_id>

      <framed_ip_address>10.20.40.10</framed_ip_address>

      ...

      <selected_azn_profiles>wired_cwa_redirect</selected_azn_profiles>

      <response_time>17</response_time>

      <cts_security_group> ADM </cts_security_group>

      <vlan>30</vlan>

      <dacl>#ACSACL#-IP-cwa_wired-4f570619</dacl>

      <endpoint_policy>WindowsXP-Workstation</endpoint_policy>

    </sessionParameters>


~~~~~~~~~~~~~~~~~~~~~~~~~
~~~ ISE ERS API Calls ~~~
~~~~~~~~~~~~~~~~~~~~~~~~~

Three ERS API calls are needed to collect the appropriate information about the TrustSec Matrix:

- Egress Matrix Cell 'Get-All' call: https://<ise_admin_node>:9060/ers/config/egressmatrixcell 

- Egress Matrix Cell 'Get-By-ID' call: https://<ise_admin_node>:9060/ers/config/egressmatrixcell/{id}

- Security Group ACL 'Get-By-ID' call: https://<ise_admin_node>:9060/ers/config/sgacl/{id}

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~ Egress Matrix 'Get-all' Call ~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The HTTP response for the Egress Matrix 'Get-all' call is returned in JSON by default and includes the number of cells that a
TrustSec Matrix has as well as the ids and names of the cells. The HTTP response body looks like follows:

{

  "SearchResult" : {

    "total" : 2,

    "resources" : [ {

      "id" : "id1",

      "name" : "name1",

      "description" : "description1"

    }, {

      "id" : "id2",

      "name" : "name2",

      "description" : "description2"

    } ],

However, this call also supports a filter:
Key: filter
Value: sgtSrcName.EQ{{srcSGT}}; sgtDstName.EQ{{srcSGT}}

So it can be called like follows to get a single intersection cell of two tags:
https://<ise_admin_node>:9060/ers/config/egressmatrixcell?filter=sgtSrcName.EQ.<srcSGT>"&filter=sgtDstName.Eq.<dstSGT>


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~ Egress Matrix 'Get-by-id' Call ~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


The HTTP response for the Egress Matrix 'Get-BY-ID' call is returned in JSON by default and includes the cell name, srcSGTid, 
DstSGTid, matrix cell status ('ENABLED', 'MONITOR' or 'DISABLED'), the name of the default rule, and a list of configured 
SGACL IDs. The HTTP response body looks like follows:

{

  "EgressMatrixCell" : {

    "sourceSgtId" : "2ebbc200-7a26-11e4-bc43-000c29ed7428",

    "destinationSgtId" : "1ebbc200-7a26-11e4-bc43-000c29ed7428",

    "matrixCellStatus" : "MONITOR",

    "defaultRule" : "PERMIT_IP",

    "sgacls" : [ "1ebbc100-7a26-11e4-bc43-000c29ed7428", "2ebbc100-7a26-11e4-bc43-000c29ed7428" ]

  }

}


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~ SGACL 'Get-by-id' Call ~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The HTTP response for the Security Group ACL 'Get-By-ID' call is returned in JSON by default and includes the SGACL ID,
the SGACL name, the SGACL description, the SGACL version, and the SGACL content. The HTTP response body looks like follows:

{

  "Sgacl" : {

    "id" : "id",

    "name" : "name",

    "description" : "description",

    "ipVersion" : "IPV4",

    "aclcontent" : "Permit IP"

  }

}

~~~~~~~~~~~~~~~~~~~
~~~ Credentials ~~~
~~~~~~~~~~~~~~~~~~~

Credentials for the 'DEV' and 'TEST' environment have values that can be configured in the config.py file. Credentials for 
the 'PROD' environment must be passed as command-line arguments. This makes it more difficult to 'accidentally' kick off the 
script towards the production environment.

To provide credentials as command-line arguments, the following parameters are available:

"-u" or "--apiusername" 
"-p" or "--apipassword"

The --apiusername and --apipassword arguments are the credentials that will be passed to the ISE API for HTTPBasic 
Authentication. For the package to work, the credentials provided must have ERS Admin and MNT Admin permissions in the 
relevant ISE environment

If the credentials are invalid, the ISE server will respond with a HTTP 401 error and the program will throw an exception
and exit once the HTTP response is received back from ISE.


~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~ Example Command Use ~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~

export $USERNAME = "ProdUser"

export $PASSWORD = "ProdPass"  

cd /[install_path]

source venv/bin/activate

python /src/SGTPolicyCheck -e Prod -u $USERNAME -p $PASSWORD -h1 R123456.mayo.edu -h2 R654321.mayo.edu


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
~~~Script Execution Output Example~~~
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
