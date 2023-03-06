import requests
import json
import datetime
import csv

def followedcount():
    date1 = datetime.datetime.now()
    with open("/home/instinctus/Desktop/run/instagram/pagetoken.txt",'r') as ptk:
        ptk = ptk.read()
        ptk = json.loads(ptk)
        ptoken = ptk['access_token']
        pid = ptk['id']

    url = "https://graph.facebook.com/v15.0/%s" %(pid)
    params = {
        "access_token":ptoken,
        "fields":"follow_count,followed_by_count,has_profile_picture,is_private,is_published,media_count,profile_pic,username"
        }
    response = requests.get(url,params=params).json()
    response['datetime'] = date1.strftime('%Y-%m-%d %H:%M:%S')
    id = date1.strftime('%Y%m%d')
    with open("/home/instinctus/Desktop/run/instagram/followedcount.csv",'w') as followedcount:
        csv_writer = csv.writer(followedcount)
        csv_writer.writerow(['id'] + list(response.keys()))
        csv_writer.writerow([id] + list(response.values()))