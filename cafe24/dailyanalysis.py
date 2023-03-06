import numpy as np
import pymysql
import time
import datetime
from dateutil.parser import parse
from dateutil import relativedelta
import csv
time1 = datetime.datetime.now()

# days
start_date = datetime.datetime(year = 2021, month = 1, day = 1).date()
end_date = datetime.datetime.now().date()
oneday = datetime.timedelta(days=1)
oneyear = relativedelta.relativedelta(years=1)
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
sql += ['''SELECT `member_id`,`payment_date` FROM `cafe24`.`orders`''']
cur.execute(sql[0])
customers = np.array(cur.fetchall())
cur.execute(sql[1])
resigneddormant = np.array(cur.fetchall())
cur.execute(sql[2])
orders = np.array(cur.fetchall())
conn.close()

print("*** PREPARING ***")
dayslen = len(days)
signin = [0 for col in range(dayslen)]
total = [0 for col in range(dayslen)]
offmemberall = np.array([x for x in resigneddormant if x[2] not in customers.T[0] and x[0] != 90146])
offmembers = np.array(['','',''])
offmemberoverlap = np.array(['','',''])
for x in offmemberall:
    if x[2] not in offmembers:
        offmembers = np.append(offmembers,x,axis=0)
    else:
        offmemberoverlap = np.append(offmemberoverlap,x,axis=0)
offmembers = False
p=0
print(len(customers),"customers")
print(len(offmemberall),"off member records")
print(len(offmemberoverlap),"offmembers overlaped")
print()
print("*** PROCESSING ***")
for i in range(0,dayslen):
    p = sum(1 for j in customers if j[1].date() == days[i])             # 현재 활성화되어 있는 회원
    for k in offmemberall:
        korders = np.array([x for x in orders if k[2] in orders.T[0]])
        if len(korders) != 0:
            if min(korders.T[1]) == days[i]:
                p+=1                                                                   # 주문내역이 있는 휴면/탈퇴 회원
        elif k[2] not in offmemberoverlap.T[2]:
            if k[1].date() - oneyear == days[i]:
                p+=1                                                                 # 휴면+탈퇴 회원
        else:
            for l in offmemberoverlap:
                if k[2] == l[2] and k[1] <= l[1]:
                    p+=1
    signin[i] = p
    print(p)
    p=0
    if i % 1 == 0:
        print(i/dayslen * 100, '% COMPLETED')

print(signin)

with open('dailyanalysis.csv','w') as dailyanalysis:
    csv_writer = csv.writer(dailyanalysis)
    csv_writer.writerow(['date','signin','total'])
    for i in range(dayslen):
        csv_writer.writerow([days[i],signin[i],total[i]])

time2 = datetime.datetime.now()
print(time2 - time1, ' elapsed')