import matplotlib.pyplot as plt
import random
import pandas as pd
from frmbook_funcs import LastYearEnd
from frmbook_funcs import GetFREDMatrix
from frmbook_funcs import TenorsFromNames
from frmbook_funcs import InterpolateCurve
#PLot 10 Hull-White paths based on yearend US Treasury curve

lastday=LastYearEnd()

seriesnames=['DGS1MO','DGS3MO','DGS6MO','DGS1',
             'DGS2','DGS3','DGS5','DGS7',
             'DGS10','DGS20','DGS30']
cdates,ratematrix=GetFREDMatrix(seriesnames,startdate=lastday,enddate=lastday)
tenorsfromtsy=TenorsFromNames(seriesnames)

#Get monhtly interpolated curve and short rate curve
tenors,curvemonthly,shortrates=InterpolateCurve(tenorsfromtsy,ratematrix[0])

#do one graph with sigma=.05 and another
#with sigma=.2
#keep track of range
minrate,maxrate=0,0
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
fig.suptitle("10 Hull-White Curves, σ=.05 and .2")
random.seed(3.14159265)

ax=ax1
for sigma in (.05,.2):
    #set parameters for Ornstein-Uhlenbeck process
    #xlambda is spring stiffness; sigma is volatility
    xlambda=1
    #generate and plot 10 sample curves
    for sample_number in range(10):
        randomwalk=[]
        curvesample=[]
        for i,rate in enumerate(shortrates):
            if i==0: # initialize
                randomwalk.append(shortrates[i])
                curvesample.append(randomwalk[i])
            else:
                deterministic=xlambda*(shortrates[i]-randomwalk[i-1])
                #multiply by delta-t
                deterministic*=(tenors[i]-tenors[i-1])
                stochastic=sigma*random.gauss(0,1)
                randomwalk.append(randomwalk[i-1]+deterministic+stochastic)
                #sample curve is average of short rate
                #random walk to this point
                cs=curvesample[i-1]*i
                cs+=randomwalk[i]
                cs/=(i+1)
                curvesample.append(cs)
        minrate=min(curvesample)
        maxrate=max(curvesample)
        ax.plot(tenors,curvesample)
    plt.xlabel('Tenor (years)')
    ax.grid(True)
    ax=ax2
## Configure the graph
plt.ylabel("Rate (%/year)")
plt.ylim(min(0,minrate),max(3,maxrate))
plt.show
