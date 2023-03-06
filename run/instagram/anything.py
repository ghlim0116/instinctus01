import requests
import json
import refreshtoken
import datetime
import csv

user_id = '670719607830408'
appid = '857805542024270'
# with open("apptoken.txt","r") as atk:
#     atk = atk.read()
#     apptoken = json.loads(atk)['access_token']
refreshtoken.refreshtoken()
with open("token.txt",'r') as token:
    token = token.read().replace("'",'"')
    token = json.loads(token)
    atoken = token['access_token']
    ig_user_id = token['user_id']



date1 = datetime.datetime.now()
with open("pagetoken.txt",'r') as ptk:
    ptk = ptk.read()
    ptk = json.loads(ptk)
    ptoken = ptk['access_token']
    pid = ptk['id']

url = "https://graph.facebook.com/v15.0/%s" %(pid)
params = {
    "access_token":ptoken,
    "fields":"followed_by_count",
    }
response = requests.get(url,params=params).json()
print(response)
with open("anything.csv",'w') as anythint:
    csv_writer = csv.writer(anythint)
    csv_writer.writerow(response.keys())
    csv_writer.writerow(response.values())