import csv
import numpy as np
import datetime
import pymysql
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score as S_index
from sklearn.metrics import calinski_harabasz_score as CH_index
from sklearn.metrics import davies_bouldin_score as DB_index
import seaborn as sns
import pickle
from dateutil.parser import parse
import sys
sys.path.append("../../log")
import log

onemonth = relativedelta(months=1)
oneyear = relativedelta(months=12)

def getrfm(time1 = datetime.datetime.now().strftime("%y-%m-01")):
    time1 = parse(time1)
    # oneyearago = (time1 - oneyear).strftime('%Y-%m-%d 00:00:00')
    oneyearago = '2022-08-09 00:00:00'

    conn = pymysql.connect(host = '172.16.2.211',port=3306,database='cafe24',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
    cur = conn.cursor()
    sql = []
    sql += ['''
        SELECT `member_id`
        FROM `cafe24`.`customers`
        WHERE (`last_login_date` > "%s" or `created_date` > "%s") and `created_date` < "%s" and `member_id` <> 'commons' and `member_id` <> 'call'
    ''' %('2021-07-26 00:00:00', '2021-07-26 00:00:00', time1)]
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
            if F > 12:
                F = 12
            if F != 0:
                R = (time1 - thecustomer_orders.T[1].max()).days
                M = sum(thecustomer_orders.T[2])
                csv_writer.writerow([thecustomer[0],R,F,M])
        
    del customers, orders, filter_order, rfmcsv

def kmeansrfm(ks = [4],showplt=False,showindex=False):
    df = pd.read_csv('rfm.csv',names=['id','R','F','M'])
    
    # elbow point
    # df_r = df[['R']]
    # df_f = df[['F']]
    # df_m = df[['M']]
    # point = {}
    # for k in range(1,10):
    #     kmeans = KMeans(n_clusters=k,max_iter=100).fit(df_m)
    #     df_r['cluster'] = kmeans.labels_
    #     point[k] = kmeans.inertia_
    # plt.plot(list(point.keys()),list(point.values()))
    # plt.show()
    
    ks = ks
    S_indices = pd.DataFrame(np.zeros(shape=(3,len(ks))),columns=ks,index=['RS','FS','MS'])
    CH_indices = pd.DataFrame(np.zeros(shape=(3,len(ks))),columns=ks,index=['RC','FC','MC'])
    DB_indices = pd.DataFrame(np.zeros(shape=(3,len(ks))),columns=ks,index=['RD','FD','MD'])
    fig, ax = plt.subplots(3,len(ks),figsize=(16,9))
    colors = [[0.13,0.09,0.23],[0.30,0.28,0.75],[0.55,0.56,0.98],[0.84,0.85,1]][::-1]
    Rmin, Rmax = 0, 366
    Fmin, Fmax = 1, 12
    Mmin, Mmax = 5000, 400000
    df_cluster = pd.DataFrame([-1 for x in range(len(df))])
    for k in range(len(ks)):
        kmeans = KMeans(n_clusters=ks[k],max_iter=100,n_init=20,random_state=10)
        df_r = df[['R']].copy()
        kmeans.fit(df_r)
        r_cluster = kmeans.predict(df_r)
        df_r['cluster'] = df_cluster
        df_r['cluster1'] = kmeans.labels_
        df_r_describe = df_r.groupby('cluster1').describe()
        df_r_describe = df_r_describe.sort_values(by=('R','max'),ascending=False)
        index_before = df_r_describe.index
        df_r_describe = df_r_describe.reset_index(drop=True)
        index_after = df_r_describe.index
        for i in range(len(df_r)):
            for j in range(len(index_before)):
                if df_r.loc[i,'cluster'] >= 0:
                    continue
                if df_r.loc[i,'cluster1'] == index_before[j]:
                    df_r.loc[i,'cluster'] = index_after[j]
        
        df_f = df[['F']].copy()
        kmeans.fit(df_f)
        f_cluster = kmeans.predict(df_f)
        df_f['cluster'] = df_cluster
        df_f['cluster1'] = kmeans.labels_
        df_f_describe = df_f.groupby('cluster1').describe()
        df_f_describe = df_f_describe.sort_values(by=('F','max'),ascending=True)
        index_before = df_f_describe.index
        df_f_describe = df_f_describe.reset_index(drop=True)
        index_after = df_f_describe.index
        for i in range(len(df_f)):
            for j in range(len(index_before)):
                if df_f.loc[i,'cluster'] >= 0:
                    continue
                if df_f.loc[i,'cluster1'] == index_before[j]:
                    df_f.loc[i,'cluster'] = index_after[j]
        
        df_m = df[['M']].copy()
        kmeans.fit(df_m)
        m_cluster = kmeans.predict(df_m)
        df_m['cluster'] = df_cluster
        df_m['cluster1'] = kmeans.labels_
        df_m_describe = df_m.groupby('cluster1').describe()
        df_m_describe = df_m_describe.sort_values(by=('M','max'),ascending=True)
        index_before = df_m_describe.index
        df_m_describe = df_m_describe.reset_index(drop=True)
        index_after = df_m_describe.index
        for i in range(len(df_m)):
            for j in range(len(index_before)):
                if df_m.loc[i,'cluster'] >= 0:
                    continue
                if df_m.loc[i,'cluster1'] == index_before[j]:
                    df_m.loc[i,'cluster'] = index_after[j]

        if showplt == True:
            ax[0,k].set_title('R %d' %ks[k])
            ax[0,k].set_xlim(Rmin,Rmax)
            for i in range(ks[k]):
                ax[0,k].hist(df_r.loc[df_r['cluster'] == i,['R']],color=colors[i],bins=np.arange(1,Rmax,5))
            
            ax[1,k].set_title('F %d' %ks[k])
            ax[1,k].set_xticks(np.arange(1,Fmax+1,1))
            ax[1,k].set_xlim(Fmin,Fmax)
            ax[1,k].set_yscale('log')
            #ax[1,k].set_xscale('log')
            for i in range(ks[k]):
                #ax[1,k].hist(df_f.loc[df_f['cluster'] == i,['F']],color=colors[2*i],bins=10**np.linspace(1,np.log10(xmax),200))
                ax[1,k].hist(df_f.loc[df_f['cluster'] == i,['F']],color=colors[i],bins=np.linspace(1,Fmax,Fmax))            
            
            ax[2,k].set_title('M %d' %ks[k])
            ax[2,k].set_xlim(Mmin,Mmax)
            # ax[2,k].set_xticks(np.arange(1,Mmax+1,200))
            # ax[2,k].set_xscale('log')
            ax[2,k].set_yscale('log')
            for i in range(ks[k]):
                # ax[2,k].hist(df_m.loc[df_m['cluster'] == i,['M']],color=colors[i],bins=10**np.linspace(np.log10(3000),np.log10(Mmax),200))
                ax[2,k].hist(df_m.loc[df_m['cluster'] == i,['M']],color=colors[i],bins=np.linspace(1,Mmax,200))
        
        if showindex == True:
            S_indices.iloc[0,k] = S_index(df_r[['R']],r_cluster)
            CH_indices.iloc[0,k] = CH_index(df_r[['R']],r_cluster)
            DB_indices.iloc[0,k] = DB_index(df_r[['R']],r_cluster)
            S_indices.iloc[1,k] = S_index(df_f[['F']],f_cluster)
            CH_indices.iloc[1,k] = CH_index(df_f[['F']],f_cluster)
            DB_indices.iloc[1,k] = DB_index(df_f[['F']],f_cluster)
            S_indices.iloc[2,k] = S_index(df_m[['M']],m_cluster)
            CH_indices.iloc[2,k] = CH_index(df_m[['M']],m_cluster)
            DB_indices.iloc[2,k] = DB_index(df_m[['M']],m_cluster)
    
    if showindex == True:
        SCD_indices = pd.concat([S_indices,CH_indices,DB_indices])
        SCD_indices.to_csv('rfmMLindex.csv',index=True)
        print(SCD_indices)
    
    df['r_grade'] = df_r['cluster']+1
    df['f_grade'] = df_f['cluster']+1
    df['m_grade'] = df_m['cluster']+1
    df.to_csv('rfmMLall.csv',index=False,)

    if showplt==True:
        plt.subplots_adjust(left=0.07,bottom=0.05,top=0.95,right=0.95,hspace=0.25)
        plt.savefig('clustering_rfm.png')
        plt.show()

def classrfmML(Nclass=4,time1 = datetime.datetime.now().strftime("%y-%m-01"),showplt=False):
    # 데이터 불러오기
    df = pd.read_csv('rfmMLall.csv',names=['id','R','F','M','r_grade','f_grade','m_grade'],skiprows=1)
    
    # raise SystemError
    sumpayment = df['M'].sum()
    lenrfm = len(df)
    # 6개 순서대로 등급별 0고객수, 1매출액, 2구성비, 3매출기여도, 4기여효과, 5기준, 6등급, 7가중치
    eff = np.zeros(shape=(3,Nclass,8))
    rfm = ['R','F','M']
    rfm_grade = ['r_grade','f_grade','m_grade']
    for i in range(Nclass):
        for j in range(3): # eff[0]: R, eff[1]: F, eff[2]: M
            eff[j,i,0] = df.groupby(by=rfm_grade[j])[rfm[j]].describe().loc[i+1,'count']
            eff[j,i,1] = df.loc[df[rfm_grade[j]] == i+1,'M'].sum()
            eff[j,i,5] = df.groupby(by=rfm_grade[j])[rfm[j]].describe().loc[i+1,'min']
            eff[j,i,2] = eff[j,i,0]/lenrfm
            eff[j,i,3] = eff[j,i,1]/sumpayment
            eff[j,i,4] = eff[j,i,3] / eff[j,i,2]
            eff[j,i,6] = i+1
    
    # 등급과 기여효과 회귀선의 기울기로 가중치 구하기
    rpf, fpf, mpf = [np.polyfit(eff[i].T[6],eff[i].T[4],1) for i in range(3)]
    rfm_weight = rpf[0] + fpf[0] + mpf[0]
    r_weight = rpf[0] / rfm_weight
    f_weight = fpf[0] / rfm_weight
    m_weight = mpf[0] / rfm_weight
    eff[0,:,7] = r_weight
    eff[1,:,7] = f_weight
    eff[2,:,7] = m_weight
    
    # RFM class 저장
    with open('rfmMLclass.csv','w') as rfmclasscsv:
        csv_writer = csv.writer(rfmclasscsv)
        rfmMLclass_header = ['date','RFM','grade','count','sales','fraction','sales_contr','contr_eff','min','weight']
        csv_writer.writerow(rfmMLclass_header)
        for j in range(3):
            for i in range(Nclass):
                csv_writer.writerow([time1] + [rfm[j]] + [int(eff[j,i,6])] + [x for x in eff[j,i,:6]] + [eff[j,i,7]])
    
    df['rfm_index'] = df['r_grade'] * r_weight + df['f_grade'] * f_weight + df['m_grade'] * m_weight
    for i in range(lenrfm):    
        if df.loc[i,'r_grade'] >= 3:
            if df.loc[i,'f_grade'] >= 3:
                if df.loc[i,'m_grade'] >= 3:
                    df.loc[i,'group'] = 'VIP'
                else:
                    df.loc[i,'group'] = 'ROYAL'
            elif df.loc[i,'m_grade'] >= 3:
               df.loc[i,'group'] = 'semi-VIP'
            else:
                df.loc[i,'group'] = 'new'
        elif df.loc[i,'m_grade'] >= 3:
            df.loc[i,'group'] = 'esc-VIP'
        else:
            df.loc[i,'group'] = 'esc'
    df['date'] = time1
    df = df[['date'] + list(df.columns[:len(df.columns)-1])]
    df.to_csv('rfmMLallindex.csv',header=True,index=False)

    # FLOT 0고객수, 1매출액, 2구성비, 3매출기여도, 4기여효과, 5기준, 6등급, 7가중치
    if showplt == True:
        fig, ax = plt.subplots(2,3,figsize=(16,9))
        for i in range(0,3):
            ax[0,i].set_xlabel("grade")
            ax[0,i].set_ylabel("sales_eff")
            ax[1,i].set_xlabel("grade")
            ax[1,i].set_ylabel("contr_eff")
            #ax[0,i].scatter(eff[i].T[6],eff[i].T[3])
            #ax[1,i].scatter(eff[0].T[6],eff[i].T[4])
        ax[0,i].set_title('R')
        ax[0,1].set_title('F')
        ax[0,2].set_title('M')
        ax[1,0].set_title('R')
        ax[1,1].set_title('F')
        ax[1,2].set_title('M')
        ax[1,1].hist(df['rfm_index'],bins=np.arange(1,4,0.1))
        ax[1,1].set_title('Index')
        plt.show()

def plotrfm(time1 = datetime.datetime.now().strftime("%y-%m-01"),showplt=True):
    df = pd.read_csv('rfmMLall.csv',names=['id','R','F','M','r_grade','f_grade','m_grade'],skiprows=1)
    Nclass = df['r_grade'].nunique()
    
    Rmin, Rmax = 0, 366
    Fmin, Fmax = 1, 12
    Mmin, Mmax = 5000, 400000
    Mticks = [10000,30000,100000,300000]
    cmap = 'gist_ncar'
    colors = [[0.13,0.09,0.23],[0.30,0.28,0.75],[0.55,0.56,0.98],[0.84,0.85,1]][::-1]
    
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
    ax0.scatter(df['R'],df['F'],df['M'], marker=".", c='#211C35', alpha=0.5, s=2)

    ax1 = fig.add_subplot(3,4,1)
    ax1.set_title('F-M Projection')
    ax1.set_xlabel('Frequency')
    ax1.set_ylabel('Monetary')
    #ax1.set_yscale('symlog')
    #ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    #ax1_yspace = np.logspace(np.log10(Mmin),np.log10(Mmax),150)
    #ax1.set_yticks(Mticks)
    ax1.set_facecolor('k')
    hist1 = ax1.hist2d(df['F'],df['M'],bins=(int(max(df['F'])),180),cmap=cmap,norm=matplotlib.colors.LogNorm())
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
    hist2 = ax2.hist2d(df['R'],df['M'],bins=(int(Rmax/3),ax2_yspace),cmap=cmap,norm=matplotlib.colors.LogNorm())
    ax2.set_ylim(Mmin, Mmax)
    fig.colorbar(hist2[3],ax=ax2)
    
    ax3 = fig.add_subplot(3,4,9)
    ax3.set_title('R-F Projection')
    ax3.set_xlabel('Recency')
    #ax3.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax3.set_ylabel('Frequency')
    ax3.set_yticks(np.arange(0,Fmax,5))
    ax3.set_facecolor('k')
    hist3 = ax3.hist2d(df['R'],df['F'],bins=(Rmax,int(max(df['F']))),cmap=cmap,norm=matplotlib.colors.LogNorm())
    ax3.set_xlim(Rmin,Rmax)
    ax3.set_ylim(Fmin,Fmax)
    fig.colorbar(hist3[3],ax=ax3)

    ax4 = fig.add_subplot(3,4,2)
    ax4.set_title('R histogram')
    ax4.set_xlabel('Recency')
    for i in range(Nclass):
        ax4.hist(df.loc[df['r_grade']==i+1,'R'],bins=(range(Rmin,Rmax,5)),color=colors[i])

    ax5 = fig.add_subplot(3,4,6)
    ax5.set_title('F histogram')
    ax5.set_xlabel('Frequency')
    ax5.set_yscale('symlog')
    for i in range(Nclass):
        ax5.hist(df.loc[df['f_grade']==i+1,'F'],bins=(range(Fmin,Fmax,1)),color=colors[i])

    ax6 = fig.add_subplot(3,4,10)
    ax6.set_title('M histogram')
    ax6.set_xlabel('Monetary')
    # ax6.set_xticks(np.arange(0,800000,200000))
    ax6.set_yscale('symlog')
    # ax6.set_xscale('log')
    for i in range(Nclass):
        # ax6.hist(df.loc[df['m_grade']==i+1,'M'],bins=(10**np.linspace(np.log10(3000),np.log10(Mmax),200)),color=colors[i])
        ax6.hist(df.loc[df['m_grade']==i+1,'M'],bins=(np.linspace(Mmin,Mmax,200)),color=colors[i])
    
    plt.subplots_adjust(left=0.05,bottom=0.05,top=0.92,right=0.95,hspace=0.35)
    plt.suptitle('RFM scatter', fontsize=16)
    pickle.dump(fig, open(time1+' rfm.fig.pickle','wb'))
    plt.savefig(time1+' rfm.image.png')
    if showplt == True:
        plt.show()

def uploadrfm():
    conn = pymysql.connect(host = '172.16.2.211',port=3306,database='cafe24',charset='utf8mb4',local_infile=1, user='root',password='skxortn1!')
    cur = conn.cursor()
    sql = []
    sql += [log.sqlquery(filename="rfmMLallindex.csv",database="cafe24",table="rfm",ignorelines="1",linedivider="\n",columns="`date`,`member_id`,`r`,`f`,`m`,`r_grade`,`f_grade`,`m_grade`,`rfm_index`,`group`")]
    sql += [log.sqlquery(filename="rfmMLclass.csv",database="cafe24",table="rfmclass",ignorelines="1",columns="`date`,`rfm`,`class`,`members`,`sales`,`fraction`,`sales_cont`,`cont_eff`,`criteria`,`weight`")]
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
    
    time1 = '2023-03-02'
    if True:
    # for time1 in time:
        getrfm(time1=time1)
        kmeansrfm(showplt=False,showindex=False)
        classrfmML(4,time1=time1,showplt=False)
        plotrfm(time1=time1,showplt=True)
        # uploadrfm()