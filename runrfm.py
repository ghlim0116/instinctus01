import logging
from dateutil.relativedelta import relativedelta
import datetime
import rfm
import sys
sys.path.append("../log")
import mail
import log
import traceback
import pymysql

stlogger = logging.getLogger("stlog")
stlogger.setLevel(logging.INFO)
logformatter = logging.Formatter('%(levelname)s %(asctime)s > %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logformatter)
stlogger.addHandler(stream_handler)

mylogger = logging.getLogger("mylog")
mylogger.setLevel(logging.INFO)
logformatter = logging.Formatter('%(filename)s,%(levelname)s,%(message)s,%(asctime)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler('log.csv', mode='w',encoding='utf-8')
file_handler.setFormatter(logformatter)
mylogger.addHandler(file_handler)

errorlogger = logging.getLogger("errorlog")
errorlogger.setLevel(logging.INFO)
logformatter = logging.Formatter('%(filename)s,%(message)s,%(asctime)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler = logging.FileHandler('errorlog.csv', mode='w',encoding='utf-8')
file_handler.setFormatter(logformatter)
errorlogger.addHandler(file_handler)

onemonth = relativedelta(months=1)
oneyear = relativedelta(months=12)

try:
    stlogger.info('RFM ANALYSIS STARTED')
    mylogger.info('%s,RFM ANALYSIS STARTED' %(log.log_no()))
    time = []
    start_yearmonth = datetime.date(year=2022,month=11,day=1)
    add_yearmonth = start_yearmonth
    while add_yearmonth < datetime.datetime.now().date():
        time += [add_yearmonth.strftime('%Y-%m-%d')]
        add_yearmonth = add_yearmonth + onemonth
    
    for time1 in time:
        print()
        stlogger.info('%s ANALYSISING' %(time1))

        stlogger.info('GET RFM DATA')
        mylogger.info('%s,GET RFM DATA' %(log.log_no()))
        rfm.getrfm(time1=time1)
        
        stlogger.info('PLOT RFM')
        mylogger.info('%s,PLOT RFM' %(log.log_no()))
        rfm.plotrfm(time1=time1,showplt=False)

        stlogger.info('RFM DATA ANALYZING')
        mylogger.info('%s,RFM DATA ANALYZING' %(log.log_no()))                
        rfm.classrfm(5,time1=time1,showplt=False)

        stlogger.info('UPLOAD RFM DATA TO MARIADB')
        mylogger.info('%s,UPLOAD RFM DATA TO MARIADB' %(log.log_no()))
        rfm.uploadrfm()
    
except Exception as e:
    errorlogno = log.log_no()
    mylogger.info('%s,%s' %(errorlogno,'"%s"' %(e)))
    stlogger.info('*** AN ERROR OCCURED ***')
    errorlogger.error('%s,%s,"%s"' %(errorlogno, '"%s"', traceback.format_exc().replace('"',"'")) %(str(e)))
    # mail.mail(subject="RFM Data Pipeline Error: %s" %(str(e)),body=traceback.format_exc().replace('"',"'"),To="geonho.lim@cheremimaka.com")
    
finally:
    print()
    stlogger.info('RFM ANALYSIS FINISHED')
    mylogger.info('%s,RFM ANALYSIS FINISHED' %(log.log_no()))
    conn = pymysql.connect(host = '172.16.2.211',port=3306,database='log',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
    cur = conn.cursor()
    sql = []
    sql += [log.sqlquery(filename="log.csv",database="log",table="log",columns="`filename`,`loglevel`,`log_no`,`message`,`datetime`",linedivider="\\n",ignorelines="0")]
    sql += [log.sqlquery(filename="errorlog.csv",database="log",table="errorlog",columns="`filename`,`log_no`,`errorname`,`tracebackmsg`,`datetime`",linedivider="\\n",ignorelines="0")]
    for s in sql:
        cur.execute(s)
    conn.commit()
    conn.close()