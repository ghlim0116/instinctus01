import requests
import json
import pandas as pd
import numpy as np
import time
import datetime
import csv
from dateutil.parser import parse
from dateutil import relativedelta
import refreshtoken

def privacy():
    time1 = datetime.datetime.now()

    atoken= refreshtoken.refresh()
    time.sleep(0.5)
    apicount = 1

    # get privacy data
    headers = {
        'Authorization': 'Bearer %s' %(atoken),
        'Content-Type': "application/json",
        'X-Cafe24-Api-Version': "2022-12-01"
        }
    url = "https://instinctus1.cafe24api.com/api/v2/admin/customersprivacy/count"
    response = requests.request("GET", url, headers=headers)
    customercount = json.loads(response.text)['count']
    print(customercount, 'customers found')
    apicount += 1
    time.sleep(0.5)

    onemonth = relativedelta.relativedelta(months=1)
    oneday = datetime.timedelta(days=1)
    start_date = datetime.datetime(year = 2015, month = 9, day = 1).date()
    # start_date = datetime.datetime(year = 2022, month = 9, day = 1).date()
    countsum = []

    def countofcustomers(start_date,headers):
        url = "https://instinctus1.cafe24api.com/api/v2/admin/customersprivacy/count?search_type=created_date&created_start_date=%s" %(start_date)
        response = requests.request("GET", url, headers=headers)
        answer = json.loads(response.text)['count']
        return answer

    start_date1 = start_date
    print("GET CUSTOMERS COUNTS")
    while True:
        countsum += [countofcustomers(start_date1,headers)]
        apicount += 1
        time.sleep(0.4)
        # print(start_date1, countsum[-1])
        start_date1 = start_date1 + onemonth
        if datetime.datetime.now().date() < start_date1:
            break

    counts = []
    for i in range(0,len(countsum)-1):
        counts += [countsum[i] - countsum[i+1]]
    counts += [countsum[-1]]
    print(counts)
    print("")
    print("WRITING STARTED")
    
    headerTF = True
    with open("customers.csv", 'w', encoding='utf-8-sig') as customers:
        csv_writer = csv.writer(customers)
        for i in counts:
            if i > 1000:
                # 한 달을 일단위로 쪼개서 count를 list에 저장한 뒤 각 구간마다 고객정보를 불러옴
                start_dates_inamonth = [start_date]
                start_date_nextmonth = start_date + onemonth
                while start_dates_inamonth[-1] < start_date_nextmonth:
                    start_dates_inamonth += [start_dates_inamonth[-1] + oneday]
                countsuminamonth = [countofcustomers(start_dates_inamonth[0],headers)]
                apicount += 1
                time.sleep(0.43)
                countsinamonth = []
                for j in range(1,len(start_dates_inamonth)):
                    countsuminamonth += [countofcustomers(start_dates_inamonth[j],headers)]
                    countsinamonth += [countsuminamonth[j-1] - countsuminamonth[j]]
                    # print(start_dates_inamonth[j-1], countsinamonth[-1])
                    apicount += 1
                    time.sleep(0.43)
                del start_dates_inamonth[-1]
                
                for j in range(0,len(countsinamonth)):
                    url = "https://instinctus1.cafe24api.com/api/v2/admin/customersprivacy?search_type=created_date&created_start_date=%s&limit=%s" %(start_dates_inamonth[j],countsinamonth[j])
                    response = requests.request("GET", url, headers=headers)
                    apicount += 1
                    time.sleep(0.45)
                    if """{"error":{"code":422,"message":"[Limit] should be between 1 and 1000. (parameter.limit)"}}""" in response.text:
                        continue
                    try:
                        customer_json = [json.loads(response.text)][0]['customersprivacy']
                    except KeyError:
                        print(response.text)
                    for row in customer_json:
                        row['created_date'] = parse(row['created_date']).strftime('%Y-%m-%d %H:%M:%S')
                        if  row['last_login_date'] != '' and row['last_login_date'] != '00-00-00 00:00:00':   
                            row['last_login_date'] = parse(row['last_login_date']).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            row['last_login_date'] = '00-00-00 00:00:00'                    
                        csv_writer.writerow(row.values())

            elif i != 0:
                url = "https://instinctus1.cafe24api.com/api/v2/admin/customersprivacy?search_type=created_date&created_start_date=%s&limit=%s" %(start_date,i)
                response = requests.request("GET", url, headers=headers)
                apicount += 1
                time.sleep(0.43)
                try:
                    customer_json = [json.loads(response.text)][0]['customersprivacy']
                    if headerTF == True:
                        csv_writer.writerow(customer_json[0].keys())
                        headerTF = False
                    for row in customer_json:
                        row['created_date'] = parse(row['created_date']).strftime('%Y-%m-%d %H:%M:%S')
                        if  row['last_login_date'] != '' and row['last_login_date'] != '00-00-00 00:00:00':   
                            row['last_login_date'] = parse(row['last_login_date']).strftime('%Y-%m-%d %H:%M:%S')
                        else:
                            row['last_login_date'] = '00-00-00 00:00:00'                    
                        csv_writer.writerow(row.values())
                except KeyError:
                    print(response.text)

            start_date = start_date + onemonth
    
    del counts, row
    time2 = datetime.datetime.now()
    print(apicount, 'APIs sent')
    print(time2 - time1, 'elapsed')