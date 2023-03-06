import logging
import traceback
import numpy as np
import datetime
import pymysql
import sys

def sqlquery(filename="",database="",table="",linedivider="\r\n",ignorelines="1",columns=""):
    sqlquery = """
        LOAD DATA LOW_PRIORITY LOCAL INFILE '%s'
        REPLACE INTO TABLE `%s`.`%s`
        CHARACTER SET utf8mb4
        FIELDS TERMINATED BY ','
        OPTIONALLY ENCLOSED BY '"'
        ESCAPED BY '"'
        LINES TERMINATED BY '%s'
        IGNORE %s LINES
        (%s);
        """ %(filename,database,table,linedivider,ignorelines,columns)
    return sqlquery

def log_no():
    rand = int(np.random.rand()*10000)
    log_no = datetime.datetime.now().strftime('%Y%m%d%H%M%S-' + str(rand))
    return log_no

if __name__ == '__main__': # 로그 기록 샘플 코드
    try:
        sys.path.append("/home/instinctus/Desktop/log")
        import mail
        import log
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
        
        stlogger.info('TRYING')
        mylogger.info('%s,TRYING' %(log.log_no()))
        # body
        stlogger.info('A LOOP FINISHED')
        mylogger.info('%s,A LOOP FINISHED' %(log.log_no()))
        
    except Exception as e:
        errorlogno = log_no()
        mylogger.info('%s,%s' %(errorlogno,e))
        stlogger.info('*** AN ERROR OCCURED ***')
        errorlogger.error('%s,%s,"%s"' %(errorlogno, str(e), traceback.format_exc().replace('"',"'")))
        
    finally:
        conn = pymysql.connect(host = '172.16.2.211',port=3306,database='log',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
        cur = conn.cursor()
        sql = []
        sql += [sqlquery(filename="log.csv",database="log",table="log",columns="`filename`,`loglevel`,`log_no`,`message`,`datetime`",linedivider="\\n",ignorelines="0")]
        sql += [sqlquery(filename="errorlog.csv",database="log",table="errorlog",columns="`filename`,`log_no`,`errorname`,`tracebackmsg`,`datetime`",linedivider="\\n",ignorelines="0")]
        for s in sql:
            cur.execute(s)
        conn.commit()
        conn.close()
        stlogger.info("A LOOP FINISHED")