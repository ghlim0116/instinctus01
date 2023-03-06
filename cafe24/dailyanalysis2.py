import numpy as np
import pymysql
import time
import datetime
from dateutil.parser import parse
from dateutil import relativedelta
import csv
import pymysql

def analysis():
#if True:
    time1 = datetime.datetime.now()

    # days
    start_date = datetime.datetime(year = 2019, month = 1, day = 1).date()
    end_date = datetime.datetime.now().date()
    oneday = datetime.timedelta(days=1)
    oneyear = relativedelta.relativedelta(years=1)
    ayearago = end_date - oneyear
    days = []
    day = start_date
    while day <= end_date:
        days += [day]
        day = day + oneday

    # get data from MariaDB
    print("*** DATA IMPORTING ***")
    conn = pymysql.connect(host = '172.16.2.211',port=3306,database='cafe24',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
    cur = conn.cursor()
    sql = []
    sql += ['''SELECT `member_id`,`created_date`,`last_login_date` FROM `cafe24`.`customers`''']
    sql += ['''SELECT `event_no`,`requested_time`,`member_id` FROM `cafe24`.`resigneddormant` where `success` = "T"''' ]
    #sql += ['''SELECT `member_id`,`payment_date` FROM `cafe24`.`orders` where `member_id`<>"" ''']
    cur.execute(sql[0])
    customers = np.array(cur.fetchall())
    cur.execute(sql[1])
    resigneddormant = np.array(cur.fetchall())
    #cur.execute(sql[2])
    #orders = np.array(cur.fetchall())
    conn.close()

    print("*** PROCESS 1/3 ***")                                # 활동 회원의 가입 정보 확인
    dayslen = len(days)
    customerlen = len(customers)
    resultsignin = np.zeros(shape=(customerlen,dayslen),dtype=int)
    resulttotal = np.zeros(shape=(customerlen,dayslen),dtype=int)
    member_id = []
    for i in range(customerlen):
        if i % 5000 == 0:
            print(round(i/customerlen*100,1),"%")
        j = (customers[i][1].date() - start_date).days
        if j >= dayslen:
            print(customers[i])
        else:
            member_id += [customers[i][0]]
            resultsignin[i][j] = 1
            if customers[i][2] == "0000-00-00 00:00:00" or customers[i][2].date() <= ayearago:
                resulttotal[i][j:j+365] = 1
            else:
                resulttotal[i][j:] = 1
     
    print("*** PROCESS 2/3 ***")                                # 휴면/탈퇴 회원의 가입일 확인
    rdlen = len(resigneddormant)
    row = np.zeros(shape=(rdlen,dayslen),dtype=int)
    resultsignin = np.append(resultsignin,row,axis=0)
    del row
    n = 0
    for member in resigneddormant:
        if n % np.trunc(rdlen/10) == 0:
            print(np.trunc(n/rdlen*100), "%")
        n += 1
        if member[0] != 90146 and member[2] not in member_id:
            i = customerlen + n - 1
            signindate = (member[1] - oneyear).date()
            j = (signindate - start_date).days
            resultsignin[i][j] = 1
    signin = resultsignin.sum(axis=0)
    del resultsignin

    print("*** PROCESS 3/3 ***")                                # 휴면/탈퇴 회원의 가입기간
    row = np.zeros(shape=(rdlen,dayslen),dtype=int)
    resulttotal = np.append(resulttotal,row,axis=0)
    del row
    n = 0
    for member in resigneddormant:
        if n % np.trunc(rdlen/10) == 0:
            print(np.trunc(n/rdlen*100), "%")
        n += 1
        if member[0] != 90146 and member[2] not in member_id:
            i = customerlen + n - 1
            signindate = (member[1] - oneyear).date()
            j = (signindate - start_date).days
            resulttotal[i][j:j+365] = 1
    total = resulttotal.sum(axis=0)
    del resulttotal, member_id

    with open('dailyanalysis.csv','w') as dailyanalysis:
        csv_writer = csv.writer(dailyanalysis)
        csv_writer.writerow(['date','signin','total'])
        for i in range(dayslen):
            csv_writer.writerow([days[i],signin[i],total[i]])
    del signin, total
    
    time2 = datetime.datetime.now()
    print(time2 - time1, ' elapsed')

if __name__ == '__main__':
    analysis()