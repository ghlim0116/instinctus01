import json
import requests
import datetime
import csv
import time
import datetime
import numpy as np
import refreshtoken

def privacyaddinfo():
#if True:
    time1 = datetime.datetime.now()
    atoken = refreshtoken.refresh()
    autho = 'bearer %s' %(atoken)
    headers = {
        'Authorization': autho,
        'Content-Type': "application/json",
        'X-Cafe24-Api-Version': "2022-09-01"
        }

    apicount = 0
    i = -1
    with open('customers.csv', 'r') as customers:
        counts = len(customers.readlines()) - 1
        print(counts, 'CUSTOMERS FOUND')

    with open('customersaddinfo.csv','w') as f:
        csv_writer = csv.writer(f)
        with open('customers.csv', 'r') as customers:
            next(customers)
            for customer in customers:
                try:
                    member_id = customer.split(',')[1]
                    url = "https://instinctus1.cafe24api.com/api/v2/admin/customersprivacy/%s" %(member_id)
                    response = requests.request("GET", url, headers=headers)
                    apicount += 1
                    time.sleep(0.4)
                
                    if i == -1:
                        customer = json.loads(response.text)['customersprivacy']['additional_information']
                        csv_writer.writerow(['member_id',list(customer[0].values())[1],list(customer[1].values())[1]])
                        i += 1
                    if 'additional_information' in response.text:
                        customer = json.loads(response.text)['customersprivacy']['additional_information']
                        csv_writer.writerow([member_id,list(customer[0].values())[2],list(customer[1].values())[2]])
                        i += 1
                except:
                    print(customer)
                if i % 540 == 0:
                    rate = np.trunc(i / counts * 100)
                    print(rate, '% COMPLETED ...')
                    atoken = refreshtoken.refresh()
                    autho = 'bearer %s' %(atoken)
                    headers = {
                        'Authorization': autho,
                        'Content-Type': "application/json",
                        'X-Cafe24-Api-Version': "2022-09-01"
                    }
                    apicount += 1
                    time.sleep(0.5)
                    

    time2 = datetime.datetime.now()
    elapsed_time = time2 - time1
    print(i, "CUSTOMERS ADDITIONAL INFORMATION IMPORTED FROM", counts, "CUSTOMERS")
    print(elapsed_time, "ELAPSED")