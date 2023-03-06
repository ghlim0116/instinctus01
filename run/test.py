import traceback
import logging
import sys
sys.path.append('/home/instinctus/Desktop/log')
import log
import pymysql

# errorlogger = logging.getLogger("errorlog")
# errorlogger.setLevel(logging.INFO)
# logformatter = logging.Formatter('%(filename)s,%(message)s,%(asctime)s', datefmt='%Y-%m-%d %H:%M:%S')
# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(logformatter)
# errorlogger.addHandler(stream_handler)
# file_handler = logging.FileHandler('testlog.csv', mode='w',encoding='utf-8')
# file_handler.setFormatter(logformatter)
# errorlogger.addHandler(file_handler)


#errorlogno = log.log_no()
#errorlogger.info('%s,%s,"%s"' %(errorlogno, str(e), traceback.format_exc().replace('"',"'")))
sql = [log.sqlquery(filename="testlog.csv",database="log",table="errorlog",columns="`filename`,`log_no`,`errorname`,`tracebackmsg`,`datetime`",linedivider="\\n",ignorelines="0")]
conn = pymysql.connect(host = '172.16.2.211',port=3306,database='log',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
cur = conn.cursor()
cur.execute(sql[0])
conn.commit()
conn.close()