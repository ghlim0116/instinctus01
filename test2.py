from dateutil.parser import parse
import matplotlib.pyplot as plt
import csv
import numpy as np
import datetime
import pymysql
from dateutil.relativedelta import relativedelta
import pandas as pd
import scipy.stats as stats
import sys
sys.path.append("../log")
import mail
import log

time1 = '2023-02-01'
df = pd.read_csv('rfmMLallindex.csv')
df['date'] = time1
df = df[['date'] + list(df.columns[:len(df.columns)-1])]
print(df.head())