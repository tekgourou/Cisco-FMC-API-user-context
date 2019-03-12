# Copyright (C) 2019  Alexandre Argeris

import sys
import getopt
import json
import requests
import datetime

# Change for your Cisco FMC hostname - username - password
server = "<YOUR FMC HOSTNAME OR IP HERE>"
username = "<YOUR API USER HERE>"
password = "<YOUR PASSWORD HERE>"

# Change this to your domain
domain = '<YOUR DOMAIN HERE>'

# LOG and DB
log_file = 'fmc_user_ip_map_api_'+server+'.log'
db_file = 'db_users_'+server+'.json'

# API PATH
api_auth_path = "/api/fmi_platform/v1/identityauth/generatetoken"
api_path = "/api/identity/v1/identity/useridentity"

print('##########################################################')
print('#                  fire-context                          #')
print('#     For LAB only, production use at your own risk      #')
print('#       aargeris@cisco.com, alexandre@argeris.net        #')
print('#                                                        #')
print('#  fire-context.py -a <add-OR-delete> -i <IP> -u <user>  #')
print('#       Make sure to modify variables in the script      #')
print('#       before running it. At your own risk.             #')
print('#       fire-context.py -h [for more details]             #')
print('##########################################################')
print()

def main(argv):
   global user
   global IP
   global action
   user = ''
   IP = ''
   action = ''
   try:
      opts, args = getopt.getopt(argv,"h:i:u:a:p",["user=","device_ip=","help=","action="])
   except getopt.GetoptError:
      print (' !! Please add and modify variables as described above !!')
      print ('    This script leverage API on Cisco FMC to add or     ')
      print ('    remove a USER/IP mapping. Please go to            ')
      print ('    Analysis/UserActivity on FMC to validate mapping.   ')
      print ('    This script can only remove USER/IP mapping added ')
      print ('    by this script. Require Python3.x, module sys,getopt')
      print ('    json,requests,datetime,tinydb.')
      print ()
      sys.exit(3)
   for opt, arg in opts:
      if opt == ('-h', '--help'):
         print ('FMC_user_add_delete.py -u <user> -i <device_ip>')
         sys.exit()
      elif opt in ("-p"):
         from tinydb import TinyDB, Query
         db = TinyDB(db_file)
         db.purge()
         db.all()
         print ('Purging db: '+db_file)
         print()
         sys.exit()
      elif opt in ("-u", "--user"):
         user = arg
      elif opt in ("-i", "--device_ip"):
         IP = arg
      elif opt in ("-a", "--action"):
         action = arg

if __name__ == "__main__":
   main(sys.argv[1:])

print('Starting script...')

# USER2ADD DB
from tinydb import TinyDB, Query
db = TinyDB(db_file)

## API post to get token ##
# GET TIME in ISO8601 format
localnow = datetime.datetime.now()
utcnow = datetime.datetime.utcnow()
tzd = localnow - utcnow
secs = tzd.days * 24 * 3600 + tzd.seconds
prefix = '+'
if secs < 0:
    prefix = '-'
    secs = abs(secs)
suffix = "%s%02d:%02d" % (prefix, secs/3600, secs/60%60)
now = localnow.replace(microsecond=0)
ISO8601="%s%s" % (now.isoformat("T","seconds"), suffix)

# Allow connection to server with a selfsigned certificate
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#API request
r = None
headers = {'Content-Type': 'application/json'}
auth_url = 'https://'+ server + api_auth_path
try:
    r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username,password), verify=False)
    auth_headers = r.headers
    auth_token = auth_headers.get('X-auth-access-token', default=None)
    if auth_token == None:
        print("auth_token not found. Exiting...")
        f = open(log_file, "a")
        f.write(ISO8601 + ",auth_token not found. Exiting..." '\n')
        sys.exit()
except Exception as err:
    print("Error in generating auth token --> " + str(err))
    f = open(log_file, "a")
    f.write(ISO8601 + ",Error in generating auth token --> " + str(err)+ '\n')
    sys.exit()

if action == 'add':
    print('User ' + user + '@' + domain + ' with IP ' + IP + ' will be ' + action)
    # GET TIME in ISO8601 format
    localnow = datetime.datetime.now()
    utcnow = datetime.datetime.utcnow()
    tzd = localnow - utcnow
    secs = tzd.days * 24 * 3600 + tzd.seconds
    prefix = '+'
    if secs < 0:
        prefix = '-'
        secs = abs(secs)
    suffix = "%s%02d:%02d" % (prefix, secs / 3600, secs / 60 % 60)
    now = localnow.replace(microsecond=0)
    ISO8601 = "%s%s" % (now.isoformat("T", "seconds"), suffix)

    # Building the access token and URL
    headers['X-auth-access-token'] = auth_token
    url = 'https://' + server + api_path
    if (url[-1] == '/'):
        url = url[:-1]

    # Bulding the json
    post_data = "{\n\n\"user\": \"" + user + "\",\n\n\"srcIpAddress\": \"" + IP + "\",\n\n\"agentInfo\": \"api\",\n\n\"timestamp\": \"" + ISO8601 + "\",\n\n\"domain\": \"" + domain + "\"\n\n}\n\n"

    # Sending the resquest to add user-ip mapping
    try:
        r = requests.post(url, data=post_data, headers=headers, verify=False)
        status_code = r.status_code
        resp = r.text
        if status_code == 201 or status_code == 202:
            print(ISO8601+" API Post was successful...")
            json_resp = json.loads(resp)
            ID = json_resp["id"]
            f = open(log_file, "a")
            f.write(
                ISO8601 + ',ADD,Username:' + user + ',DeviceIP:' + IP + ',Domain:' + domain + ',SessionID:' + ID + '\n')
            db.insert({'TIME': ISO8601, 'Username': user, 'DeviceIP': IP, 'Domain': domain, 'SessionID': ID})
            print('SessionID: ' + ID + 'was added to DB :'+db_file)
            print('Details has been record in log file: '+log_file)
            print()
            f.close()
        else:
            r.raise_for_status()
            print("Error occurred in POST --> " + resp)
            f = open(log_file, "a")
            f.write(ISO8601 + ',Error occurred in POST -->' + resp + '\n')
    except requests.exceptions.HTTPError as err:
        print("Error in connection --> " + str(err))
        f = open(log_file, "a")
        f.write(ISO8601 + ',Error occurred in POST -->' + str(err) + '\n')
    finally:
        if r: r.close()

elif action == 'delete':
    # Retrive SessionID from DB
    if  db.get((Query()['Username'] == user) & (Query()['DeviceIP'] == IP)) is None:
        print('No session found for user '+user+' with '+IP+' in DB: ' + db_file)
        print()
        sys.exit()
    else:
        result = db.get((Query()['Username'] == user) & (Query()['DeviceIP'] == IP))
        sessionID = (result.get('SessionID'))
        print('Session found for ' + user + ' using IP ' + IP + ' SessionID ' + sessionID)

    # GET TIME in ISO8601 format
    localnow = datetime.datetime.now()
    utcnow = datetime.datetime.utcnow()
    tzd = localnow - utcnow
    secs = tzd.days * 24 * 3600 + tzd.seconds
    prefix = '+'
    if secs < 0:
        prefix = '-'
        secs = abs(secs)
    suffix = "%s%02d:%02d" % (prefix, secs / 3600, secs / 60 % 60)
    now = localnow.replace(microsecond=0)
    ISO8601 = "%s%s" % (now.isoformat("T", "seconds"), suffix)

    headers['X-auth-access-token'] = auth_token
    url = 'https://' + server + api_path + '/' + sessionID
    if (url[-1] == '/'):
        url = url[:-1]

    try:
        r = requests.delete(url, headers=headers, verify=False)
        status_code = r.status_code
        resp = r.text
        if status_code == 200 or status_code == 201 or status_code == 202:
            json_resp = json.loads(resp)
            f = open(log_file, "a")
            f.write(ISO8601 + ',DELETE,SessionID: ' + sessionID + '\n')
            print(ISO8601 + " API Post was successful DELETE SessionID " + sessionID)
            db.remove((Query()['Username'] == user) & (Query()['DeviceIP'] == IP))
            print('SessionID ' + sessionID + ' delete from the DB'+ db_file)
            print('Details has been record in log file: ' + log_file)
            print()
            f.close()
        else:
            r.raise_for_status()
            print("Error occurred in POST --> " + resp)
    except requests.exceptions.HTTPError as err:
        print("Error in connection --> " + str(err))
    finally:
        if r: r.close()
