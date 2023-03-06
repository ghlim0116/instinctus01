import csv
import datetime
import json
import time
import numpy as np
import pandas as pd
import requests
from dateutil import relativedelta
import refreshtoken
from dateutil.parser import parse

def webhooklog():
    time1 = datetime.datetime.now()

    # get webhooks logs
    access_token= refreshtoken.refresh()
    onemonth = relativedelta.relativedelta(months=1)
    oneday = datetime.timedelta(days=1)
    requested_end_date =  datetime.datetime.now().date()
    requested_start_date = requested_end_date - oneday * 7

    webhook_header = [
        "log_id",
        "log_type",
        "event_no",
        "event_name",
        "mall_id",
        "trace_id",
        "requested_time",
        "request_endpoint",
        "event_shop_no",
        "member_id",
        "success",
        "response_http_code",
        "response_body"
    ]
    
    headers = {
        'Authorization': "Bearer %s" %(access_token),
        'Content-Type': "application/json",
        'X-Cafe24-Api-Version': "2022-09-01"
    }
    with open("webhooklogs.csv", 'w', encoding='utf-8-sig') as webhooklogs:
        write = csv.DictWriter(webhooklogs, fieldnames= webhook_header)
        write.writeheader()

        url = "https://instinctus1.cafe24api.com/api/v2/admin/webhooks/logs?requested_start_date=%s&requested_end_date=%s&limit=10000" %(requested_start_date,requested_end_date)
        response = requests.request("GET", url, headers=headers)
        apicount = 1
        time.sleep(0.35)
        logs = json.loads(response.text.replace("\\","").replace('"{','{').replace('}"','}'))['logs']
        for row in logs:
            event_name = ''
            if row['event_no'] == 90145:
                event_name = '휴면'
            elif row['event_no'] == 90146:
                event_name = '휴면해제'
            elif row['event_no'] == 90147:
                event_name = '탈퇴'
            else:
                event_name = ''
            write.writerow(
                {
                    "log_id":row['log_id'],
                    "log_type":row['log_type'],
                    "event_no":row['event_no'],
                    "event_name":event_name,
                    "mall_id":row['mall_id'],
                    "trace_id":row['trace_id'],
                    "requested_time":parse(row['requested_time']).strftime('%y-%m-%d %H:%M:%S'),
                    "request_endpoint":row['request_endpoint'],
                    "event_shop_no":row['request_body']['resource']['event_shop_no'],
                    "member_id":row['request_body']['resource']['member_id'],
                    "success":row['success'],
                    "response_http_code":row['response_http_code'],
                    "response_body":row['response_body']
                }
            )
    del webhooklogs, logs
    time2 = datetime.datetime.now()
    print(apicount, 'APIs sent')
    print(time2 - time1, 'elapsed')