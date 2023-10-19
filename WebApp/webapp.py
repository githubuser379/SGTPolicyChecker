import os
import subprocess
from flask import Flask,render_template,request,redirect,url_for

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app= Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/sgtpolicychecker', methods=['GET','POST'])
def load_sgtpolicycheck_page():
    return render_template('sgtpolicychecker.html')

@app.route('/sgtpolicychecker/processor')
def run_sgtpolicychecker():
    host1identifiertype = request.form['host1_identifiertype']
    host2identifiertype = request.form['host2_identifiertype']

    

    ipaddr1 = request.form['ipaddress1']
    ipaddr2 = request.form['ipaddress2']
    hostname1 = request.form['hostname1']
    hostname2 = request.form['hostname2']

if __name__ == '__main__':
    app.run(debug=True)