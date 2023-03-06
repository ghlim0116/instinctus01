import numpy as np
import time
import datetime
import requests
import csv
import pymysql
import sys
sys.path.append('/home/instinctus/Desktop/run/naver')
import signaturehelper

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, secret_key)
    return {'Content-Type': 'application/json; charset=UTF-8', 'X-Timestamp': timestamp, 'X-API-KEY': api_key, 'X-Customer': str(customer_id), 'X-Signature': signature}

def naverqc():
    BASE_URL = 'https://api.searchad.naver.com'
    API_KEY = '0100000000c51d2923cd8745d9f4faf1daccd7b14423f6c314bce85c769e0c30b38c53e96c'
    SECRET_KEY = 'AQAAAADFHSkjzYdF2fT68drM17FEqLRUWKac99NI3SHqQbEhdw=='
    CUSTOMER_ID = '829946'
    method = 'GET'
    uri = '/keywordstool'
    oneday = datetime.timedelta(days=1)

    time1 = datetime.datetime.now()

    # get data from MariaDB
    conn = pymysql.connect(host = '172.16.2.211',port=3306,database='keywordqc',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
    cur = conn.cursor()
    sql = '''SELECT `keywords` FROM `keywordqc`.`keywords`'''
    cur.execute(sql)
    keywords = np.array(cur.fetchall())
    conn.close()

    # stats

    with open('/home/instinctus/Desktop/run/naver/relkeyword.csv','w') as relkeywordcsv:
        csv_writer = csv.writer(relkeywordcsv)
        headerTF = False
        for id in keywords:
            response = requests.get(
                BASE_URL + uri,
                params={
                    "hintKeywords":id,
                    "showDetail":1
                },
                headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID)
            )
            time.sleep(0.2)
            stat = response.json()['keywordList'][0]

            if headerTF == False:
                csv_writer.writerow(['date','portal'] + list(stat.keys()) + ['sumQcCnt'])
                headerTF = True
            statlist = [0 if "<" in str(a) else a for a in list(stat.values())]
            csv_writer.writerow([time1.date() - 30 * oneday,'네이버'] + statlist + [statlist[1] + statlist[2]])

    # UPLOAD DATA TO MARIADB
    sql = """
    LOAD DATA LOW_PRIORITY LOCAL INFILE '/home/instinctus/Desktop/run/naver/relkeyword.csv'
    REPLACE INTO TABLE `keywordqc`.`relkeyword`
    CHARACTER SET utf8mb4
    FIELDS TERMINATED BY ','
    OPTIONALLY ENCLOSED BY '"'
    ESCAPED BY '"'
    LINES TERMINATED BY '\r\n'
    IGNORE 1 LINES
    (`date`,`portal`,`relKeyword`,`monthlyPcQcCnt`,`monthlyMobileQcCnt`,`monthlyAvePcClkCnt`,`monthlyAveMobileClkCnt`,`monthlyAvePcCtr`,`monthlyAveMobileCtr`,`plAvgDepth`,`compIdx`,`sumQcCnt`);
    """

    conn = pymysql.connect(host = '172.16.2.211',port=3306,database='keywordqc',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    conn.close()

    
if __name__ == '__main__':
    naverqc()