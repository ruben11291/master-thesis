"""This script makes a plot representing the bandwith of a node in front of the time"""

from pylab import *
import numpy as np
import sys

def plot_bandwith(file):
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
    average_bandwith=0
    for i in bandwith:
        average_bandwith+=i
    average_bandwith = average_bandwith/len(bandwith)
    average=[]
    stdp=[] #standar deviation positive
    stdn =[] #standard deviation negative
    sd = np.std(bandwith)
    for i in bandwith:
        average.append(average_bandwith)
        stdp.append(average_bandwith+sd)
        stdn.append(average_bandwith-sd)

    plt.xlabel("Time (s)")
    plt.ylabel("Bandwith (Kb)")
    plt.plot(time[:-1],bandwith[:-1],"r",label="Bandwith")
    plt.plot(time[:-1],average[:-1],"b",label="Average")
    plt.plot(time[:-1],stdp[:-1],"g",label="Standard deviation")
    plt.plot(time[:-1],stdn[:-1],"g")
    plt.legend()
    plt.show()

if __name__=="__main__":
    if len(sys.argv) < 2:
        print "Error with arguments. You must enter at least a file"
    try:
        f = open(sys.argv[1],"r")
    except IOError as e:
        print e
        if f:
            f.close()
        exit(-1)

    plot_bandwith(f)

    f.close()
