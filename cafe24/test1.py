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

def correcttime(timex):
    if  timex == '' or timex == None:
        timex = '0000-00-00 00:00:00'
    else:
        timex = parse(timex).strftime('%Y-%m-%d %H:%M:%S')
    return timex

#def coupon():
if True:
    time1 = datetime.datetime.now()

    atoken= refreshtoken.refresh()
    time.sleep(0.5)
    apicount = 1

    # get coupon data
    headers = {
        'Authorization': 'Bearer %s' %(atoken),
        'Content-Type': "application/json",
        'X-Cafe24-Api-Version': "2022-09-01"
        }
    url = "https://instinctus1.cafe24api.com/api/v2/admin/coupons"
    response = requests.request("GET", url, headers=headers)
    coupons_json = json.loads(response.text)['coupons']
    apicount += 1
    time.sleep(0.5)

    onemonth = relativedelta.relativedelta(months=1)
    oneday = datetime.timedelta(days=1)

    # COUPONS
    headerTF = True
    couponid = [6070400403200001561]
    couponname = ["🍒피팬티 러버🍒를 위한 특별 할인쿠폰"]
    issuedcount = [7]
    createddate = ["2021-09-06 13:40:31"]
    with open("coupons.csv", 'w', encoding='utf-8-sig') as coupons:
        csv_writer = csv.writer(coupons)
        if headerTF == True:
            csv_writer.writerow(coupons_json[0].keys())
            headerTF = False
        for row in coupons_json:
            couponid += [row['coupon_no']]
            couponname += [row['coupon_name']]
            issuedcount += [int(row['issued_count'])]
            createddate += [row['created_date']]
            row['created_date'] = parse(row['created_date']).strftime('%Y-%m-%d %H:%M:%S')
            row['pause_begin_datetime'] = correcttime(row['pause_begin_datetime'])
            row['pause_end_datetime'] = correcttime(row['pause_end_datetime'])
            row['issue_order_start_date'] = correcttime(row['issue_order_start_date'])
            row['issue_order_end_date'] = correcttime(row['issue_order_end_date'])
            row['issue_reserved_date'] = correcttime(row['issue_reserved_date'])
            row['available_begin_datetime'] = correcttime(row['available_begin_datetime'])
            row['available_end_datetime'] = correcttime(row['available_end_datetime'])
            if row['available_product_list'] != None:
                row['available_product_list'] = ';'.join(map(str,row['available_product_list']))
            csv_writer.writerow(row.values())
    
    # COUPON ISSUES
    couponissuecount = 0
    onecouponissuecount = 0
    lastcouponno = ""
    headerTF = True
    with open("couponissues.csv", 'w', encoding='utf-8-sig') as couponissues:
        csv_writer = csv.writer(couponissues)
        for i in range(0,len(couponid)):
            print(couponname[i],"발급 수: ", issuedcount[i])
            if issuedcount[i] <= 8000:
                offset = issuedcount[i]
                start_date = None
                end_date = None
                searchdate = ""
            else:
                offset = 8000
                start_date = parse(createddate[i]).date()
                end_date = start_date + onemonth
                searchdate = "&issued_start_date=%s&issued_end_date=%s" %(start_date,end_date)

            while True:
                while True:
                    for j in range(0,offset,500):
                        url = "https://instinctus1.cafe24api.com/api/v2/admin/coupons/%s/issues?limit=500&offset=%s%s%s" %(couponid[i],j,searchdate,lastcouponno)
                        response = requests.request("GET", url, headers=headers)
                        time.sleep(0.42)
                        apicount += 1
                        try:
                            couponissues_json = json.loads(response.text)['issues']
                            couponissuecount += len(couponissues_json)
                            onecouponissuecount += len(couponissues_json)
                            if headerTF == True:
                                csv_writer.writerow(couponissues_json[0].keys())
                                headerTF = False
                            for row in couponissues_json:
                                row['issued_date'] = correcttime(row['issued_date'])
                                row['expiration_date'] = correcttime(row['expiration_date'])
                                row['used_date'] = correcttime(row['used_date'])
                                csv_writer.writerow(row.values())
                            if len(couponissues_json) != 500:
                                break
                        except:
                            print(response.text)
                    if len(couponissues_json) == 500:
                        lastcouponno = "&since_issue_no=" + couponissues_json[-1]['issue_no']
                    else:
                        lastcouponno = ""
                        break
                if onecouponissuecount < issuedcount[i] and onecouponissuecount != 0:
                    start_date, end_date = start_date + onemonth, end_date + onemonth
                else:
                    onecouponissuecount = 0
                    break

    print("couponissuecount =",couponissuecount)
    del couponid, couponname, issuedcount, createddate, coupons_json
    time2 = datetime.datetime.now()
    print(apicount, 'APIs sent')
    print(time2 - time1, 'elapsed')
    