"""This script makes a plot representing the bandwith of a node in front of the time"""

from pylab import *
import os
from scipy.stats import norm
import numpy as np
import sys
import pdb
import matplotlib as mpl
mpl.rcParams['axes.labelsize']=2
mpl.rcParams['axes.labelweight']=2
mpl.rcParams['font.size']=4.5
#mpl.rcParams['axes.xmargin']=2
#mpl.rcParams['axes.ymargin']=2
mpl.rcParams['figure.subplot.wspace']=0.4
mpl.rcParams['figure.subplot.hspace']=0.4
mpl.rcParams['figure.subplot.bottom']=0.0
mpl.rcParams['savefig.bbox']='tight'

#plt.set_figsize_inches(1024,872)
def plot_bandwith(file,subplot):
    bandwith = []
    time = []
    for line in file:
        l = line.split(",")
        if len(l) == 9: #the it is a client report
            transfered=l[7]
            Bps=float(l[8])
            time_=l[6].split('-')[0]
            if (Bps > 0.0):
                bandwith.append(Bps/1000)
                time.append(time_)
        else:
            #the server's report
            total_trans=l[7]
            average_bandwith=l[8]
            jitter=l[9]
            loss=l[10]
            total_pack=l[11]
            loss_rate =l[12]
    # average_bandwith=0
    # for i in bandwith:
    #     average_bandwith+=i
    # average_bandwith = average_bandwith/len(bandwith)
    # average=[]
    # stdp=[] #standar deviation positive
    # stdn =[] #standard deviation negative
    # sd = np.std(bandwith)
    # for i in bandwith:
    #     average.append(average_bandwith)
    #     stdp.append(average_bandwith+sd)
    #     stdn.append(average_bandwith-sd)

    # print "Average ", average_bandwith, "SD ",sd
    #plt.xlabel("Time (s)")
    #plt.ylabel("Bandwith (Kb)")
    #plt.plot(time[:-1],bandwith[:-1],"r.",label="Bandwith")
    #plt.plot(time[:-1],average[:-1],"b",label="Average")
    #plt.plot(time[:-1],stdp[:-1],"g",label="Standard deviation")
    #plt.plot(time[:-1],stdn[:-1],"g")
    #plt.legend()
    (mu,sigma) = norm.fit(bandwith[:-1])
    #print mu, sigma

   # plt.subplot(340+current)
   # plt.subplots(nrows=4,ncols=3)
    n , bins , patches = subplot.hist(bandwith[:-1], 30,normed=True,facecolor='green',alpha=1)
    #print bins
    #y = mlab.normpdf(bins,average_bandwith,sd)
    y = mlab.normpdf(bins,mu,sigma)
   # plt.xlabel("Bandwidth (Mbps)",fontsize=15)
    subplot.set_xlabel("Bandwidth (Mbps)",fontsize=4.5,style='italic')

    #subplot.plot(bins,y,'b-')
    subplot.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *np.exp( - (bins - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')
   # subplot.subplots_adjust(left=0.15)
    #print file.name.split(":")[0].split("/")[1]
    print file.name.split(":")[0].split("/")[1]
    subplot.set_title(r'$\mathrm{Histogram\ of\ GS\ %s:}\ \mu=%.3f,\ \sigma=%.3f$' %(file.name.split(":")[0].split("/")[1],mu, sigma),fontsize=6)
    subplot.grid(True)
    #subplot.tight_layout()
    #savefig(file.name.split(":")[0].split("/")[1]+"GS"+".png")
    #plt.show()

if __name__=="__main__":
    if len(sys.argv) < 2:
        print "Error with arguments. You must enter at least a file"
    try:
        fig, subplots = plt.subplots(nrows=4,ncols=3)
        gfx=[]
        for pl in subplots:
            for element in pl:
                gfx.append(element)

        #pdb.set_trace()
        for fileinput in os.listdir(os.sys.argv[1]):
            f = open(os.sys.argv[1]+"/"+fileinput,"r")
            plot_bandwith(f,gfx.pop())
        #plt.show()
        savefig("GSGraph"+".png",bbox_inches='tight',dpi=300)

    except IOError as e:
        print e
        if f:
            f.close()
        exit(-1)

    f.close()