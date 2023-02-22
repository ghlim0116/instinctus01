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

a = np.array([-1 for a in range(10)])
df = pd.DataFrame(a,columns=['x'])
print(len(df))

