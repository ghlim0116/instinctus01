import google
import pymysql
import time
import datetime
from dateutil.parser import parse
import sys
sys.path.append('/home/instinctus/Desktop/run/GA4')
sys.path.append('/home/instinctus/Desktop/log')
import getdata
import log

onehour = datetime.timedelta(hours=1)
oneday = datetime.timedelta(days=1)
#date1 = ""                                                          # 시작일:"2022-08-18"
def ga4():                                                         ### 특정 날짜의 데이터를 불러올 때
    date1 = (datetime.datetime.now().date() - oneday).strftime("%Y-%m-%d")
    while date1 != datetime.datetime.now().strftime('%Y-%m-%d'):    ### 여러 날짜의 데이터를 불러올 때
        try:
            # 'date1' in 'YYYY-MM-DD' format pulls data of the date.
            # Empty date pulls yesterday's.
            getdata.run_report(date1=date1)

            sql = []
            sql += [log.sqlquery(filename="/home/instinctus/Desktop/run/GA4/hour.csv",database="ga4",table="hour",linedivider="\r\n",ignorelines="1",columns="`date`,`hour`,`screenpageviews`,`screenpageviewspersession`,`ecommercepurchases`,`purchasetoviewrate`,`activeusers`,`totalPurchasers`,`sessions`,`purchaserConversionRate`,`sessionsConversionRate:purchase`,`userConversionRate:purchase`,`userconversionrate_view_item`,`userconversionrate_scroll`")]
            sql += [log.sqlquery(filename="/home/instinctus/Desktop/run/GA4/item.csv",database="ga4",table="item",linedivider="\r\n",ignorelines="1",columns="`date`,`itemname`,`itemsviewed`,`itemsPurchased`,`purchaseToViewRate`,`totalPurchasers`,`activeUsers`,`userConversionRate:view_item`")]
            sql += [log.sqlquery(filename="/home/instinctus/Desktop/run/GA4/landingpage.csv",database="ga4",table="landingpage",linedivider="\r\n",ignorelines="1",columns="`date`,`landingPage`,`sessions`,`screenPageViewsPerSession`,`activeUsers`,`purchaseConversionRate`,`totalPurchasers`,`userconversionrate_view_item`,`userconversionrate_scroll`")]
            sql += [log.sqlquery(filename="/home/instinctus/Desktop/run/GA4/page.csv",database="ga4",table="page",linedivider="\r\n",ignorelines="1",columns="`date`,`pagepath`,`pagetitle`,`screenpageviews`,`bouncerate`,`engagementRate`,`userEngagementDuration`,`averageSessionDuration`,`userconversionrate_scroll`")]
            sql += [log.sqlquery(filename="/home/instinctus/Desktop/run/GA4/scrolldepth.csv",database="ga4",table="scrolldepth",linedivider="\r\n",ignorelines="1",columns="`date`,`pagepath`,`percentScrolled`,`sessions`,`screenPageViews`,`screenPageViewsPerSession`")]
            sql += [log.sqlquery(filename="/home/instinctus/Desktop/run/GA4/searchterm.csv",database="ga4",table="searchterm",linedivider="\r\n",ignorelines="1",columns="`date`,`searchterm`,`activeUsers`")]
            sql += [log.sqlquery(filename="/home/instinctus/Desktop/run/GA4/sourcemedium.csv",database="ga4",table="sourcemedium",linedivider="\r\n",ignorelines="1",columns="`date`,`source`,`medium`,`sourcePlatform`,`activeUsers`")]
            
            conn = pymysql.connect(host = '172.16.2.211',port=3306,database='ga4',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
            cur = conn.cursor()
            for cmd in sql:
                cur.execute(cmd)
            conn.commit()
            conn.close()

            if date1:
                # print(date1, "COMPLETED")
                date1 = (parse(date1).date() + oneday).strftime('%Y-%m-%d')
            #else:
        except google.api_core.exceptions.ResourceExhausted:
            print("**        GA4 TOKEN EXHAUSETED        **")
            print("**           RETRY NEXT TIME          **")
            time.sleep(60)
    
if __name__ == '__main__':
    ga4()