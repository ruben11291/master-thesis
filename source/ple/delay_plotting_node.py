"""This script makes a plot representing the bandwith of a node in front of the time"""


gs={"Canada":"Prince Albert" , "Argentina": "Cordoba","Australia":"Sydney","Brazil":"Kourou","China":"Irkutsk","Florida":"Chetumal","Israel":"Dubai","Malaysia":"Malaysia","New Zealand":"Troll","Norway":"Svalbard","Reunion Island":"Krugersedorp","Spain":"Puertollano"}


from pylab import *
import os
from scipy.stats import norm
import numpy as np
import sys
import pdb
import matplotlib as mpl
mpl.rcParams['axes.labelsize']=2
mpl.rcParams['axes.labelweight']=2
mpl.rcParams['font.size']=12

mpl.rcParams['savefig.bbox']='tight'

#plt.set_figsize_inches(1024,872)
def plot_delay(file):

    delays=[]
    for line in file:
        if line.find("time") != -1:
            if line[line.find("time")+4]=='=':
                data =line.split("time")[1].split("=")[1].split(" ")[0]
                delays.append(float(data))
    (mu,sigma) = norm.fit(delays)
    print mu, sigma


    n , bins , patches = plt.hist(delays, 15,normed=True,facecolor='green',alpha=1)
    #print bins
    #y = mlab.normpdf(bins,average_bandwith,sd)
    y = mlab.normpdf(bins,mu,sigma)
   # plt.xlabel("Bandwidth (Mbps)",fontsize=15)
    plt.xlabel("Delay (ms)",fontsize=13,style='italic')
    plt.ylabel("Ocurrence probability",fontsize=13,style='italic')
    data1=frange(140,180,0.3)

    #subplot.plot(bins,y,'b-')
    plt.plot(data1, 1/(sigma * np.sqrt(2 * np.pi)) *np.exp( - (data1 - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')
    print file.name.split(":")[0].split("/")[1]
    plt.title(r'$\mathrm{Histogram\ of\ GS\ %s:}\ \mu=%.3f,\ \sigma=%.3f$' %(gs[file.name.split(":")[0].split("/")[1]],mu, sigma),fontsize=16)
    plt.grid(True)
    plt.tight_layout()
    #savefig(file.name.split(":")[0].split("/")[1]+"GS"+".png")
    #plt.show()

if __name__=="__main__":
    if len(sys.argv) < 2:
        print "Error with arguments. You must enter at least a file"
    try:

        f = open(os.sys.argv[1],"r")
        plot_delay(f)
        #plt.show()
        savefig("DelayHistGS"+gs[os.sys.argv[1].split(":")[0].split("/")[1]]+".pdf",bbox_inches='tight',dpi=300)

    except IOError as e:
        print e
        if f:
            f.close()
        exit(-1)

    f.close()
