"""This script makes a plot representing the bandwith of a node in front of the time"""

from pylab import *
import sys

def plot_bandwith(file):
    bandwith = []
    time = []
    for line in file:
        l = line.split(",")
        if len(l) == 9: #the it is a client report 
            transfered=l[7]
            Bps=l[8]
            time_=l[6].split('-')[0]
            bandwith.append(float(Bps)/1000)
            time.append(time_)
        else:
            #the server's report 
            total_trans=l[7]
            average_bandwith=l[8]
            jitter=l[9]
            loss=l[10]
            total_pack=l[11]
            loss_rate =l[12]
        #bandwith.append(line.split(
    x = np.linspace(float(time[0]),float(time[-1]))
    print x,bandwith
    x = np.linspace(-100,100)
    #plt.plot(time[:-1],bandwith[:-1],"r")
    plt.plot(x,x**2)
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
