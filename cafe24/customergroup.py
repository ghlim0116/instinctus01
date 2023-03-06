import json
import requests
import datetime
import csv
import time
import datetime
import numpy as np
import refreshtoken

def customergroup():
    time1 = datetime.datetime.now()

    atoken = refreshtoken.refresh()
    autho = 'bearer %s' %(atoken)
    headers = {
    'Authorization': autho,
    'Content-Type': "application/json",
    'X-Cafe24-Api-Version': "2022-09-01"
    }

    cg_header = [
        'shop_no',
        'group_no',
        'group_name',
        'group_description',
        'group_icon',
        'benefits_paymethod',
        'buy_benefits',
        'ship_benefits',
        'product_availability',
        'mileage',
        'discount'
    ]

    url = "https://instinctus1.cafe24api.com/api/v2/admin/customergroups"
    response = requests.request("GET", url, headers=headers)
    a = json.loads(response.text)['customergroups']

    with open('customergroups.csv','w') as customergroups:
        write = csv.DictWriter(customergroups, fieldnames= cg_header)
        write.writeheader()
        for row in a:
            try:
                mileage = row["points_information"]["amount_discount"]
            except:
                mileage = 0
            try:
                discount = row["discount_information"]["amount_discount"]
            except:
                discount = 0
            write.writerow(
                {
                    "shop_no":row["shop_no"],
                    "group_no":row["group_no"],
                    "group_name":row["group_name"],
                    "group_description":row["group_description"],
                    "group_icon":row["group_icon"],
                    "benefits_paymethod":row["benefits_paymethod"],
                    "buy_benefits":row["buy_benefits"],
                    "ship_benefits":row["ship_benefits"],
                    "product_availability":row["product_availability"],
                    "mileage":mileage,
                    "discount":discount
                }
            )
            
    time2 = datetime.datetime.now()
    print(time2 - time1, 'elapsed')
