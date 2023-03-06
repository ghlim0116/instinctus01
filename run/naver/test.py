import numpy as np
import time
import datetime
import requests
import csv
import signaturehelper
import pymysql
from dateutil.parser import parse

oneday = datetime.timedelta(days=1)

# get data from MariaDB
# conn = pymysql.connect(host = '172.16.2.211',port=3306,database='keywordqc',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
# cur = conn.cursor()
# sql = '''SELECT * FROM `keywordqc`.`relkeyword`'''
# cur.execute(sql)
# relkeywords = np.array(cur.fetchall())
# conn.close()

# with open('test.csv','w') as testcsv:
#     csv_writer = csv.writer(testcsv)
#     for row in relkeywords:
#         if row[0] > datetime.date(2022,11,1):
#             row[0] = row[0] - 30 * oneday
#         csv_writer.writerow(row)


# UPLOAD DATA TO MARIADB
sql = """
LOAD DATA LOW_PRIORITY LOCAL INFILE 'test.csv'
REPLACE INTO TABLE `keywordqc`.`relkeyword`
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 0 LINES
(`date`,`portal`,`relKeyword`,`monthlyPcQcCnt`,`monthlyMobileQcCnt`,`monthlyAvePcClkCnt`,`monthlyAveMobileClkCnt`,`monthlyAvePcCtr`,`monthlyAveMobileCtr`,`plAvgDepth`,`compIdx`,`sumQcCnt`);
"""

conn = pymysql.connect(host = '172.16.2.211',port=3306,database='keywordqc',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
cur = conn.cursor()
cur.execute(sql)
conn.commit()
conn.close()