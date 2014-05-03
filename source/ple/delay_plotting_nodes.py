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
mpl.rcParams['font.size']=7
#mpl.rcParams['axes.xmargin']=2
#mpl.rcParams['axes.ymargin']=2
mpl.rcParams['figure.subplot.wspace']=0.4
mpl.rcParams['figure.subplot.hspace']=0.4
mpl.rcParams['figure.subplot.bottom']=0.0
mpl.rcParams['savefig.bbox']='tight'

#plt.set_figsize_inches(1024,872)
def plot_delay(file,node):

    delays=[]
    for line in file:
        if line.find("time") != -1:
            if line[line.find("time")+4]=='=':
                data =line.split("time")[1].split("=")[1].split(" ")[0]
                delays.append(float(data))
    (mu,sigma) = norm.fit(delays)
    print mu, sigma


    #plt.plot(node,mu,"o")
    plt.errorbar(node,mu,yerr=sigma,label=r"Node %d: $\mu=%3.f,\ \sigma=%.3f$"%(node,mu,sigma),fmt=".",barsabove=True)

    plt.xlabel("Nodes",fontsize=7,style="italic")
    plt.ylabel("Delay (Ms)",fontsize=7,style="italic")
    plt.title('Delay per node')
    #plt.annotate(r"$\mu=%3.f,\ \sigma=%.3f$"%(mu,sigma),(node,mu+sigma))
    plt.grid(True)
    plt.tight_layout()
    #plt.legend(title=
    plt.legend(ncol=2,shadow=True,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize=10)
    #plt.set_figwidth(20)
    #plt.autoscale(enable=True, axis='both', tight=True)
#savefig(file.name.split(":")[0].split("/")[1]+"GS"+".png")
    #plt.show()
    #plt.xlim(xmin=-1,xmax=13)#x limits

   # plt.ylim(ymin=mu-sigma-2)#y limit
    #plt.ylim(ymax=mu+sigma+2)

if __name__=="__main__":
    if len(sys.argv) < 2:
        print "Error with arguments. You must enter at least a file"
    try:
        #pdb.set_trace()
        node=1
        for directory in sys.argv[1:]:
            for fileinput in os.listdir(directory):
                f = open(directory+"/"+fileinput,"r")
                plot_delay(f,node)
                node+=1
        #plt.show()
        savefig("DelayNodes"+".png",bbox_inches='tight',dpi=300)

    except IOError as e:
        print e
        if f:
            f.close()
        exit(-1)

    f.close()
