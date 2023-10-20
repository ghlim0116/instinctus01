import time
import datetime
import requests
import csv
import signaturehelper
import pymysql

time1 = datetime.datetime.now()

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': API_KEY, 'X-Customer': str(CUSTOMER_ID), 'X-Signature': signature}

BASE_URL = 'https://api.naver.com'
API_KEY = ''
SECRET_KEY = ''
CUSTOMER_ID = ''

# campaign
uri = '/ncc/campaigns'
method = 'GET'
response = requests.get(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
campaign = response.json()

with open ('campaign.csv','w') as campaigncsv:
    csv_writer = csv.writer(campaigncsv)
    csv_writer.writerow(campaign[0].keys())
    for row in campaign:
        csv_writer.writerow(row.values())

print("*** CAMPAINGS IMPORTED ***")

# adgroups
uri = '/ncc/adgroups'
method = 'GET'
response = requests.get(BASE_URL + uri, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
adgroup = response.json()

with open ('adgroup.csv','w') as adgroupcsv:
    csv_writer = csv.writer(adgroupcsv)
    csv_writer.writerow(adgroup[0].keys())
    for row in adgroup:
        csv_writer.writerow(row.values())

print("*** ADGROUPS IMPORTED ***")

# keywords
uri = '/ncc/keywords'
method = 'GET'
headerTF = False
keywordids = []
with open ('keyword.csv','w') as keywordcsv:
    csv_writer = csv.writer(keywordcsv)
    for ag in adgroup:
        response = requests.get(BASE_URL + uri, params={'nccAdgroupId': ag['nccAdgroupId']}, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
        keyword = response.json()
        if headerTF == False:
            csv_writer.writerow(keyword[0].keys())
            headerTF = True
        for row in keyword:
            csv_writer.writerow(row.values())
            keywordids += [[row['nccKeywordId'],row['keyword']]]
            

print("*** KEYWORDS IMPORTED ***")

# stats
uri = '/stats'
method = 'GET'
headerTF = False
with open ('stat.csv','w') as statcsv:
    csv_writer = csv.writer(statcsv)
    for id in keywordids:
        response = requests.get(
            BASE_URL + uri,
            params={
                "ids": id[0],
                "fields": """["clkCnt","impCnt","salesAmt", "ctr", "cpc", "avgRnk", "ccnt", "viewCnt"]""",
                "timeRange": """{"since":"2022-10-01","until":"2022-10-31"}"""
            },
            headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID)
        )
        stat = response.json()
        if len(stat['data']) !=0 :
            if headerTF == False:
                csv_writer.writerow(['keyword'] + list(stat['data'][0].keys()))
                headerTF = True
            csv_writer.writerow([id[1]] + list(stat['data'][0].values()))

print("*** STATS IMPORTED ***")

del adgroup, keyword, stat

time2 = datetime.datetime.now()
print()
print("A LOOP FINISHED AT", time2.strftime('%Y-%m-%d %H:%M:%S'))
print(time2 - time1, ' elapsed')
