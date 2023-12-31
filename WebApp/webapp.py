import os
import subprocess
from flask import Flask,render_template,request,redirect,url_for

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def load_loginpage():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        auth_result = ""
        return render_template('login.html',result = auth_result)

@app.route('/sgtpolicychecker', methods=['GET'])
def load_sgtpolicycheck_page():
    return render_template('sgtpolicychecker.html')

@app.route('/sgtpolicychecker/results', methods=['GET','POST'])
def run_sgtpolicychecker():
    output = ""
    if request.method == 'POST':
        host1identifiertype = request.form['host1_identifiertype']
        host2identifiertype = request.form['host2_identifiertype']
        iseenvironment = request.form['iseenvironment']
        host1argtype = ""
        host1value = ""
        host2argtype = ""
        host2value = ""

        if host1identifiertype == "hostname":
            hostname1 = request.form['host1']
            host1argtype = "--hostname1"
            host1value = str(hostname1)
        elif host1identifiertype == "ipaddress":
            ipaddress1 = request.form['host1']
            host1argtype = "--ipaddress1"
            host1value = str(ipaddress1)
        if host2identifiertype == "hostname":
            hostname2 = request.form['host2']
            host2argtype = "--hostname2" 
            host2value = str(hostname2)
        elif host2identifiertype == "ipaddress":
            ipaddress2 = request.form['host2']
            host2argtype = "--ipaddress2" 
            host2value = str(ipaddress2)
        
        sgtpolicycheck_path = os.path.join(os.path.dirname(os.getcwd()),'SGTPolicyCheck')
        if iseenvironment == "dev":
            sgtpolicycheck_command = subprocess.run(["python",sgtpolicycheck_path,"--environment","Dev",host1argtype,host1value,host2argtype,host2value],capture_output=True, text=True)
        elif iseenvironment == "test":
            sgtpolicycheck_command = subprocess.run(["python",sgtpolicycheck_path,"--environment","Test",host1argtype,host1value,host2argtype,host2value],capture_output=True, text=True)
        elif iseenvironment == "prod":
            apiusername = os.environ.get('SGTPOLICYCHECK_USERNAME')
            print(apiusername)
            apipassword = os.environ.get('SGTPOLICYCHECK_PASSWORD')
            print(apipassword)
            sgtpolicycheck_command = subprocess.run(["python",sgtpolicycheck_path,"--environment","Prod",host1argtype,host1value,host2argtype,host2value,"--apiusername",apiusername,"--apipassword",apipassword],capture_output=True, text=True)

        if sgtpolicycheck_command.returncode == 0:
            output = sgtpolicycheck_command.stdout
        else:
            output = sgtpolicycheck_command.stderr

    return render_template('sgtpolicychecker.html',result=output)
    
if __name__ == '__main__':
    app.run(debug=True)