import csv
import numpy as np
import datetime
import pymysql
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import pickle
from dateutil.parser import parse
import sys
sys.path.append("../../log")
import log

def uploadrfm():
    conn = pymysql.connect(host = '172.16.2.211',port=3306,database='cafe24',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
    cur = conn.cursor()
    sql = []
    sql += [log.sqlquery(filename="mid rfmMLallindex.csv",database="cafe24",table="rfmrebranding",ignorelines="1",linedivider="\n",columns="`date`,`member_id`,`r`,`f`,`m`,`r_grade`,`f_grade`,`m_grade`,`rfm_index`,`group`")]
    sql += [log.sqlquery(filename="mid rfmMLclass.csv",database="cafe24",table="rfmrebrandingclass",ignorelines="1",columns="`date`,`rfm`,`class`,`members`,`sales`,`fraction`,`sales_cont`,`cont_eff`,`criteria`,`weight`")]
    for s in sql:
        cur.execute(s)
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    uploadrfm()