import requests
import json
import refreshtoken
import csv
from dateutil.parser import parse

refreshtoken.refreshtoken()
with open("token.txt",'r') as token:
    token = token.read().replace("'",'"')
token = json.loads(token)
atoken = token['access_token']
ig_user_id = token['user_id']

url = "https://graph.instagram.com/v15.0/%s/media" %(ig_user_id)
params = {
    'access_token':atoken,
    'fields':'id,media_type,media_url,username,timestamp,caption'
    }
response = requests.get(url,params=params).json()['data']
with open("media.csv",'w') as media:
    csv_writer = csv.writer(media)
    csv_writer.writerow(response[0].keys())
    for data in response:
        data['timestamp'] = parse(data['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        csv_writer.writerow(data.values())