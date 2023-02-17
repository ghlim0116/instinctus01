import csv
import numpy as np
import datetime
import pymysql
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler as scaler
import seaborn as sns
import pickle
from dateutil.parser import parse
import scipy.stats as stats
import sys
sys.path.append("../log")
import log

onemonth = relativedelta(months=1)
oneyear = relativedelta(months=12)

def getrfm(time1 = datetime.datetime.now().strftime("%y-%m-01")):
    times = datetime.datetime.now()
    time1 = parse(time1)
    oneyearago = (time1 - oneyear).strftime('%Y-%m-%d 00:00:00')

    conn = pymysql.connect(host = '172.16.2.211',port=3306,database='cafe24',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
    cur = conn.cursor()
    sql = []
    sql += ['''
        SELECT `member_id`
        FROM `cafe24`.`customers`
        WHERE (`last_login_date` > "%s" or `created_date` > "%s") and `member_id` <> 'commons' and `member_id` <> 'call'
    ''' %(oneyearago, oneyearago)]
    cur.execute(sql[0])
    customers = np.array(cur.fetchall())
    print(len(customers),"CUSTOMERS FOUND")
    filter_order = customers.T.tolist()
    filter_order = "','".join(filter_order[0])
    filter_order = "('" + filter_order + "')"
    sql += ['''
        SELECT `member_id`,`payment_date`,`payment_amount`
        FROM `cafe24`.`orders`
        WHERE `order_price_amount` > 0 and `member_id` in %s and "%s" > `payment_date` and `payment_date` > "%s"
    ''' %(filter_order,time1,oneyearago)]
    cur.execute(sql[1])
    orders = np.array(cur.fetchall())
    conn.close()

    R, F, M = 0,0,0
    with open('rfm.csv','w') as rfmcsv:
        csv_writer = csv.writer(rfmcsv)
        for thecustomer in customers:
            filter = np.asarray([thecustomer])
            thecustomer_orders = orders[np.in1d(orders[:,0],filter)]
            F = len(thecustomer_orders)        
            if F != 0:
                R = (time1 - thecustomer_orders.T[1].max()).days
                M = sum(thecustomer_orders.T[2])
                csv_writer.writerow([thecustomer[0],R,F,M])
        
    del customers, orders, filter_order, rfmcsv
    timef = datetime.datetime.now()
    elapsed_time = timef - times
    print(elapsed_time, "elapsed")

def kmeansrfm():
    ks = [3,4,5,6]
    df = pd.read_csv('rfm.csv',names=['id','R','F','M'])
    df_ = df[['R','F','M']]
    df_scale = scaler.transform(df_)
    
    fig = plt.figure(figsize=(9,9),projection='3d')
    ax = np.zeros(shape=(2,2))
    for i in range(4):
        ax[.0]
    for k in ks:
        kmeans = KMeans(n_clusters=k,max_iter=100,n_init='auto',random_state=10)
        kmeans.fit(df_scale)
        df_['cluster'] = kmeans.fit_predict(df_scale)
        for i in range(k):
            axc = k-3
            ax[axc//2,axc%2] 
        continue


def plotrfm(time1 = datetime.datetime.now().strftime("%y-%m-01"),showplt=True):
    with open('rfm.csv','r') as rfmcsv:
        R, F, M = [], [], []
        data = list(csv.reader(rfmcsv))
    for x in data:
        R += [float(x[1])]
        F += [float(x[2])]
        M += [float(x[3])]
    del data
    
    Rmin, Rmax = 0, 366
    Fmin, Fmax = 1, 11
    Mmin, Mmax = 5000, 400000
    Mticks = [10000,30000,100000,300000]
    cmap = 'gist_ncar'
    
    fig= plt.figure(figsize=(16,9))
    ax0 = fig.add_subplot(1,2,2, projection='3d')
    ax0.set_title('3D distribution')
    ax0.set_xlabel('Recency')
    #ax0.set_xlim(Rmin, Rmax)
    ax0.set_ylabel('Frequency')
    ax0.set_ylim(Fmin, Fmax)
    ax0.set_zlabel('Monetary')
    ax0.set_zlim(Mmin, Mmax)
    #ax0.set_zticks(Mticks)
    #ax0.set_zscale('symlog')
    #ax0.get_zaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    #ax0.zaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    ax0.scatter(R,F,M, marker=".", c='#211C35', alpha=0.5, s=2)
    
    ax1 = fig.add_subplot(3,4,1)
    ax1.set_title('F-M Projection')
    ax1.set_xlabel('Frequency')
    ax1.set_ylabel('Monetary')
    #ax1.set_yscale('symlog')
    #ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    #ax1_yspace = np.logspace(np.log10(Mmin),np.log10(Mmax),150)
    #ax1.set_yticks(Mticks)
    ax1.set_facecolor('k')
    hist1 = ax1.hist2d(F,M,bins=(int(max(F)),180),cmap=cmap,norm=matplotlib.colors.LogNorm())
    ax1.set_xlim(Fmin,Fmax)
    ax1.set_ylim(Mmin, Mmax)
    fig.colorbar(hist1[3],ax=ax1)
        
    ax2 = fig.add_subplot(3,4,5)
    ax2.set_title('R-M Projection')
    ax2.set_xlabel('Recency')
    #ax2.set_xlim(Rmin, Rmax)
    ax2.set_xticks(np.arange(0,Rmax,50))
    ax2.set_ylabel('Monetary')
    ax2.set_yscale('symlog')
    ax2.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax2.set_yticks(Mticks)
    ax2_yspace = np.logspace(np.log10(Mmin),np.log10(Mmax),100)
    ax2.set_facecolor('k')
    hist2 = ax2.hist2d(R,M,bins=(int(Rmax/3),ax2_yspace),cmap=cmap,norm=matplotlib.colors.LogNorm())
    ax2.set_ylim(Mmin, Mmax)
    fig.colorbar(hist2[3],ax=ax2)
    
    ax3 = fig.add_subplot(3,4,9)
    ax3.set_title('R-F Projection')
    ax3.set_xlabel('Recency')
    #ax3.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax3.set_ylabel('Frequency')
    ax3.set_yticks(np.arange(0,Fmax,5))
    ax3.set_facecolor('k')
    hist3 = ax3.hist2d(R,F,bins=(Rmax,int(max(F))),cmap=cmap,norm=matplotlib.colors.LogNorm())
    ax3.set_xlim(Rmin,Rmax)
    ax3.set_ylim(Fmin,Fmax)
    fig.colorbar(hist3[3],ax=ax3)

    ax4 = fig.add_subplot(3,4,2)
    ax4.set_title('R histogram')
    ax4.set_xlabel('Recency')
    ax4.hist(R,bins=(range(Rmin,Rmax,10)),color='#211C35')

    ax5 = fig.add_subplot(3,4,6)
    ax5.set_title('F histogram')
    ax5.set_xlabel('Frequency')
    ax5.set_yscale('symlog')
    ax5.hist(F,bins=(range(Fmin,Fmax,1)),color='#211C35')

    ax6 = fig.add_subplot(3,4,10)
    ax6.set_title('M histogram')
    ax6.set_xlabel('Monetary')
    ax6.set_xticks(np.arange(0,800000,200000))
    ax6.set_yscale('symlog')
    ax6.hist(M,bins=(range(Mmin,Mmax,5000)),color='#211C35')
    
    plt.subplots_adjust(left=0.05,bottom=0.05,top=0.92,right=0.95,hspace=0.35)
    plt.suptitle('RFM scatter', fontsize=16)
    pickle.dump(fig, open(time1+' rfm.fig.pickle','wb'))
    plt.savefig(time1+'  rfm.image.png')
    if showplt == True:
        plt.show()
    
def classrfm(Nclass=10,time1 = datetime.datetime.now().strftime("%y-%m-01"),showplt=False):
    # 데이터 불러오기
    with open('rfm.csv','r') as rfmcsv:
        rfm_o = np.empty(shape=(0,3))
        data = list(csv.reader(rfmcsv))
        member = []
        for x in data:
            if float(x[3]) != 0:
                member += [x[0]]
                rfm_o = np.append(rfm_o,np.array([[float(x[1]),float(x[2]),float(x[3])]]),axis=0)
    Nclass = Nclass
    lenrfm = len(rfm_o)
    sumpayment = sum(rfm_o.T[2])
    rfm_o = np.append(rfm_o,np.zeros(shape=(lenrfm,3)),axis=1)
    rfm = rfm_o.copy()

    # RFM 등급 분류
    percentage,percentile = np.zeros(shape=(Nclass)),np.zeros(shape=(Nclass))
    for i in range(1,Nclass):
        #percentage[i] = sum([x for x in range(Nclass-i+1,Nclass+1)])/sum([x for x in range(1,Nclass+1)]) # 1:2:3: ... :(N-1):N
        percentage[i] = i/Nclass    # 일정 비율
        if round(percentage[i] * lenrfm,4) == int(percentage[i] * lenrfm) and percentage[i] != 0:
            percentile[i] = int(percentage[i] * lenrfm) - 1
        else:
            percentile[i] = int(percentage[i] * lenrfm)

    # R/F/M 등급 기준
    rfm_criteria = np.zeros(shape=(Nclass,3,3))
    for l in range(3): # l=0:R, l=1:F, l=2:M
        if l == 0:
            rfm = np.array(sorted(rfm,key=lambda x: (x[0],x[1],x[2]))[::-1])       # R이 겹치면 F,M으로 한 번 더 정렬해줌
        elif l == 1:
            rfm = np.array(sorted(rfm,key=lambda x: (x[1],x[2],x[0])))             # F가 겹치면 M,R로 한 번 더 정렬해줌
        elif l == 2:
            rfm = np.array(sorted(rfm,key=lambda x: (x[2],x[1],x[0])))             # M이 겹치면 F,R로 한 번 더 정렬해줌
        j = 0
        for i in range(lenrfm):
            if j < Nclass and i == int(percentile[j]):
                for k in range(3):
                    rfm_criteria[j,l,k] = rfm[i,k]
                j += 1
            rfm[i,l+3] = j
    
    # RFM_o에 멤버 순서에 맞게 등급 저장
    for i in range(lenrfm):
        rfm_o[i,3],rfm_o[i,4],rfm_o[i,5] = 1, 1, 1
        for j in range(Nclass-1,-1,-1):
            if rfm_o[i,0] < rfm_criteria[j,0,0] or (rfm_o[i,0] == rfm_criteria[j,0,0] and rfm_o[i,1] > rfm_criteria[j,0,1]) or (rfm_o[i,0] == rfm_criteria[j,0,0] and rfm_o[i,1] == rfm_criteria[j,0,1] and rfm_o[i,2] >= rfm_criteria[j,0,2]):
                rfm_o[i,3] = j+1
                break
        for j in range(Nclass-1,-1,-1):
            if rfm_o[i,1] > rfm_criteria[j,1,1] or (rfm_o[i,1] == rfm_criteria[j,1,1] and rfm_o[i,2] > rfm_criteria[j,1,2]) or (rfm_o[i,1] == rfm_criteria[j,1,1] and rfm_o[i,2] == rfm_criteria[j,1,2] and rfm_o[i,0] <= rfm_criteria[j,1,0]):
                rfm_o[i,4] = j+1
                break
        for j in range(Nclass-1,-1,-1):
            if rfm_o[i,2] > rfm_criteria[j,2,2] or (rfm_o[i,2] == rfm_criteria[j,2,2] and rfm_o[i,1] > rfm_criteria[j,2,1]) or (rfm_o[i,2] == rfm_criteria[j,2,2] and rfm_o[i,1] == rfm_criteria[j,2,1] and rfm_o[i,0] <= rfm_criteria[j,2,0]):
                rfm_o[i,5] = j+1
                break
    rfm = rfm_o.copy()
    
    # 6개 순서대로 등급별 0고객수, 1매출액, 2구성비, 3매출기여도, 4기여효과, 5기준, 6등급, 7가중치
    reff,feff,meff = np.zeros(shape=(Nclass,8)),np.zeros(shape=(Nclass,8)),np.zeros(shape=(Nclass,8))
    for i in range(Nclass):
        reff[i,0] = sum([1 for x in rfm.T[3] if x == Nclass-i])
        reff[i,1] = sum([x[2] for x in rfm if x[3] == Nclass-i])
        reff[i,2] = reff[i,0]/lenrfm
        reff[i,3] = reff[i,1]/sumpayment
        reff[i,4] = reff[i,3] / reff[i,2]
        reff[i,5] = rfm_criteria[Nclass-i-1,0,0]
        reff[i,6] = Nclass-i
        feff[i,0] = sum([1 for x in rfm.T[4] if x == Nclass-i])
        feff[i,1] = sum([x[2] for x in rfm if x[4] == Nclass-i])
        feff[i,2] = feff[i,0]/lenrfm
        feff[i,3] = feff[i,1]/sumpayment
        feff[i,4] = feff[i,3] / feff[i,2]
        feff[i,5] = rfm_criteria[Nclass-i-1,1,1]
        feff[i,6] = Nclass-i
        meff[i,0] = sum([1 for x in rfm.T[5] if x == Nclass-i])
        meff[i,1] = sum([x[2] for x in rfm if x[5] == Nclass-i])
        meff[i,2] = meff[i,0]/lenrfm
        meff[i,3] = meff[i,1]/sumpayment
        meff[i,4] = meff[i,3] / meff[i,2]
        meff[i,5] = rfm_criteria[Nclass-i-1,2,2]
        meff[i,6] = Nclass-i
    
    reff = np.array([x for x in reff if x[0] != 0])
    feff = np.array([x for x in feff if x[0] != 0])
    meff = np.array([x for x in meff if x[0] != 0])    

    # 등급과 매출기여도 회귀선의 기울기로 가중치 구하기
    rpf = np.polyfit(reff.T[6],reff.T[3],1)
    fpf = np.polyfit(feff.T[6],feff.T[3],1)
    mpf = np.polyfit(meff.T[6],meff.T[3],1)
    rfm_weight = rpf[0] + fpf[0] + mpf[0]
    r_weight = rpf[0] / rfm_weight
    f_weight = fpf[0] / rfm_weight
    m_weight = mpf[0] / rfm_weight
    reff[:,7] = r_weight
    feff[:,7] = f_weight
    meff[:,7] = m_weight
    
    # RFM 등급 저장
    with open('rfmall.csv','w') as rfmallcsv:
        csv_writer = csv.writer(rfmallcsv)
        rfm_index = []
        for i in range(lenrfm):
            rfm_index += [rfm[i,3] * r_weight + rfm[i,4] * f_weight + rfm[i,5] * m_weight]
            csv_writer.writerow([time1] + [member[i]] + [int(x) for x in rfm[i]] + [rfm_index[i]])
    
    # RFM class 저장
    with open('rfmclass.csv','w') as rfmclasscsv:
        csv_writer = csv.writer(rfmclasscsv)
        for i in range(Nclass):
            csv_writer.writerow([time1] + ["R"] + [int(reff[i,6])] + [x for x in reff[i,:6]] + [reff[i,7]])
            csv_writer.writerow([time1] + ["F"] + [int(feff[i,6])] + [x for x in feff[i,:6]] + [feff[i,7]])
            csv_writer.writerow([time1] + ["M"] + [int(meff[i,6])] + [x for x in meff[i,:6]] + [meff[i,7]])
    
    # FLOT 0고객수, 1매출액, 2구성비, 3매출기여도, 4기여효과, 5기준, 6등급, 7가중치
    fig, ax = plt.subplots(2,3,figsize=(16,9))
    for i in range(0,3):
        ax[0,i].set_xlabel("grade")
        ax[0,i].set_ylabel("sales_eff")
        ax[1,i].set_xlabel("grade")
        ax[1,i].set_ylabel("contr_eff")
    ax[0,0].scatter(reff.T[6],reff.T[3])
    ax[0,0].set_title('R')
    ax[0,1].scatter(feff.T[6],feff.T[3])
    ax[0,1].set_title('F')
    ax[0,2].scatter(meff.T[6],meff.T[3])
    ax[0,2].set_title('M')
    ax[1,0].scatter(reff.T[6],reff.T[4])
    ax[1,0].set_title('R')
    ax[1,1].scatter(feff.T[6],feff.T[4])
    ax[1,1].set_title('F')
    ax[1,2].scatter(meff.T[6],meff.T[4])
    ax[1,2].set_title('M')
    #ax[1,1].hist(rfm_index,bins=np.arange(1,11,1))
    #ax[1,1].set_title('Index')
    if showplt == True:
        plt.show()

def uploadrfm():
    conn = pymysql.connect(host = '172.16.2.211',port=3306,database='cafe24',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
    cur = conn.cursor()
    sql = []
    sql += [log.sqlquery(filename="rfmall.csv",database="cafe24",table="rfm",ignorelines="0",columns="`date`,`member_id`,`r`,`f`,`m`,`r_grade`,`f_grade`,`m_grade`,`rfm_index`")]
    sql += [log.sqlquery(filename="rfmclass.csv",database="cafe24",table="rfmclass",ignorelines="0",columns="`date`,`rfm`,`class`,`members`,`sales`,`fraction`,`sales_cont`,`cont_eff`,`criteria`,`weight`")]
    for s in sql:
        cur.execute(s)
    conn.commit()
    conn.close()
    
if __name__ == '__main__':
    time = []
    start_yearmonth = datetime.date(year=2022,month=11,day=1)
    add_yearmonth = start_yearmonth
    while add_yearmonth < datetime.datetime.now().date():
        time += [add_yearmonth.strftime('%Y-%m-%d')]
        add_yearmonth = add_yearmonth + onemonth
    
    time1 = '2023-02-01'
    if True:
    #for time1 in time:
        #getrfm(time1=time1)
        kmeansrfm()
        #plotrfm(time1=time1,showplt=False)
        #classrfm(5,time1=time1,showplt=False)
        #uploadrfm()