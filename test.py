import time
import numpy as np
from dateutil.relativedelta import relativedelta
import datetime
import matplotlib.pyplot as plt
import matplotlib
from scipy import interpolate

Rmin, Rmax = 1, 20
Mmin, Mmax = 10000, 700000
Mticks = [10000,30000,100000,300000]

R = np.random.uniform(0,1,10000)
R = np.trunc(R * (Rmax-Rmin) + Rmin)
M = np.random.rand(10000)
M = np.log10(M*9+1)*690000+10000

fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(1,2,1)
ax1.set_title('R-M Projection')
ax1.set_xlabel('Recency')
ax1.set_xlim(Rmin, Rmax)
ax1.set_xticks(np.arange(Rmin,Rmax,1))
ax1.set_ylabel('Monetary')
ax1.set_ylim(Mmin, Mmax)
ax1.set_yscale('symlog')
ax1.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax1.set_yticks(Mticks)
ax1.set_facecolor('k')
ax1_yspace = np.logspace(np.log10(Mmin),np.log10(Mmax),150)
Result, Rhist, Mhist, histtype = ax1.hist2d(R,M,bins=(20,ax1_yspace),cmap=matplotlib.cm.jet,norm=matplotlib.colors.LogNorm())

ax3 = fig.add_subplot(1,2,2)
ax3.set_title('R-M Interpolation')
ax3.set_xlabel('Recency')
ax3.set_xlim(Rmin, Rmax)
ax3.set_xticks(np.arange(Rmin,Rmax,1))
ax3.set_ylabel('Monetary')
ax3.set_ylim(Mmin, Mmax)
ax3.set_yscale('symlog')
ax3.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
ax3.set_yticks(Mticks)

# fig.colorbar(f3,ax=ax3)
XX = Rhist[:-1]
YY = Mhist[:-1]

print(XX,YY)
itpf = interpolate.RegularGridInterpolator([XX,YY],Result,method='cubic',fill_value=0)
Xnew = np.linspace(Rmin,Rmax,200)
Ynew = np.logspace(Mmin,Mmax,200)
#Znew = itpf(Xnew,Ynew)
#f3 = ax3.contourf(Xnew,Ynew,Znew,cmap='jet')#,colors='k',levels=7,linestyles=':',linewidths=1)
plt.show()
