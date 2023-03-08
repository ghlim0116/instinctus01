from GA4 import ga4
from instagram import instagram
from naver import naverqc
import logging
import datetime
import time
import traceback
import pymysql
import sys
sys.path.append('/home/instinctus/Desktop/log')
import log
import mail

oneminute = datetime.timedelta(minutes=1)
onehour = datetime.timedelta(hours=1)
oneday = datetime.timedelta(days=1)

stlogger = logging.getLogger("stlog")
stlogger.setLevel(logging.INFO)
logformatter = logging.Formatter('''%(levelname)s %(asctime)s > %(message)s''', datefmt='%Y-%m-%d %H:%M:%S')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logformatter)
stlogger.addHandler(stream_handler)

mylogger = logging.getLogger("mylog")
mylogger.setLevel(logging.INFO)
logformatter = logging.Formatter('''%(filename)s,%(levelname)s,%(message)s,%(asctime)s''', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler('log.csv', mode='w',encoding='utf-8')
file_handler.setFormatter(logformatter)
mylogger.addHandler(file_handler)

errorlogger = logging.getLogger("errorlog")
errorlogger.setLevel(logging.INFO)
logformatter = logging.Formatter('''%(filename)s,%(message)s,%(asctime)s''', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler('errorlog.csv', mode='w',encoding='utf-8')
file_handler.setFormatter(logformatter)
errorlogger.addHandler(file_handler)

while True:
    try:
        time1 = datetime.datetime.now()    

        mylogger.info('%s,GET GA4 DATA' %(log.log_no()))
        stlogger.info('*             GET GA4 DATA            *')
        ga4.ga4()
        mylogger.info('%s,GA4 DATA IMPORTED' %(log.log_no()))
        stlogger.info('*          GA4 DATA IMPORTED          *')

        mylogger.info('%s,GET INSTAGRAM DATA' %(log.log_no()))
        stlogger.info('*          GET INSTAGRAM DATA         *')
        instagram.instagram()
        mylogger.info('%s,INSTAGRAM DATA IMPORTED' %(log.log_no()))
        stlogger.info('*       INSTAGRAM DATA IMPORTED       *')
        
        mylogger.info('%s,GET NAVER QC DATA' %(log.log_no()))
        stlogger.info('*          GET NAVER QC DATA          *')
        naverqc.naverqc()
        mylogger.info('%s,NAVER QC DATA IMPORTED' %(log.log_no()))
        stlogger.info('*        NAVER QC DATA IMPORTED       *')
        
        stlogger.info("*           A LOOP FINISHED           *")
        mylogger.info('%s,A LOOP FINISHED' %(log.log_no()))
        
    except Exception as e:
        errorlogno = log.log_no()
        mylogger.info('''%s,"%s"''' %(errorlogno,e))
        stlogger.info('* !!!!!!!!! AN ERROR OCCURED !!!!!!!!! *')
        errorlogger.error('%s,"%s","%s"' %(errorlogno, str(e), traceback.format_exc().replace('"',"'")))
        mail.mail(subject="GIN Data Pipeline Error: %s" %(str(e)),body=traceback.format_exc().replace('"',"'"),To=["geonho.lim@cheremimaka.com"])
    finally:
        conn = pymysql.connect(host = '172.16.2.211',port=3306,database='log',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
        cur = conn.cursor()
        sql = []
        sql += [log.sqlquery(filename="log.csv",database="log",table="log",columns="`filename`,`loglevel`,`log_no`,`message`,`datetime`",linedivider="\\n",ignorelines="0")]
        sql += [log.sqlquery(filename="errorlog.csv",database="log",table="errorlog",columns="`filename`,`log_no`,`errorname`,`tracebackmsg`,`datetime`",linedivider="\\n",ignorelines="0")]
        for s in sql:
            cur.execute(s)
        conn.commit()
        conn.close()
        nexttime = (time1 + onehour).replace(minute=59,second=0)
        time2 = datetime.datetime.now()
        elapsed_time = (time2 - time1).total_seconds()
        stlogger.info("*         %s SECONDS ELAPSED       *" %('{:05.2f}'.format(elapsed_time)))
        stlogger.info("*     RECUR AT %s    *" %(nexttime.strftime("%Y-%m-%d %H:%M:%S")))
        stlogger.info("%s" %("* "* 20))
        time.sleep((nexttime - time2).total_seconds())