"""This script makes a plot representing the bandwith of a node in front of the time"""

dst={"France":0,"Switzerland":1,"Belgium":2,"Netherlands":3,"Spain":4,"Germany":5,"Italy":6,"Czech Republic":7,"United Kingdom":8,"Ireland":9,"Portugal":10,"Hungary":11,"Poland":12,"Norway":13,"Greece":14,"Sweden":15,"Finland":16,"Israel":17,"Russian Federation":18,"Canada":19,"Florida":20,"United States":20,"China":21,"Brazil":22,"Korea, Republic of":23,"Reunion Island":24,"Thailand":25,"Hong Kong":26,"Japan":27,"Malaysia":28,"Singapore":29,"Argentina":30,"Australia":31,"New Zealand":32}
distances={"France":308,"Switzerland":464,"Belgium":503,"Spain2":538,"Netherlands":693,"Spain":801.50,"Germany":815,"Italy":957,"Czech Republic":1061,"United Kingdom":1091,"Ireland":1093,"Portugal":1138,"Hungary":1319,"Poland":1381,"Norway":1635,"Greece":1783,"Sweden":1882,"Finland":2298,"Israel":3265,"Russian Federation":6220,"Canada":6840,"Florida":7665,"United States":7665,"China":8021,"Brazil":8624,"Korea, Republic of":9192,"Reunion Island":9208,"Thailand":9395,"Hong Kong":9773,"Japan":9849,"Malaysia":10414,"Singapore":10786,"Argentina":11464,"Australia":15158,"New Zealand":19178}
SpainNodes={"138.4.0.120":"Spain" , "213.73.40.106":"Spain2"}

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

distances_=[]
delays_=[]
sigmas_=[]

#plt.set_figsize_inches(1024,872)
def plot_delay(file,node,distance,outfile):

    delays=[]
    for line in file:
        if line.find("time") != -1:
            if line[line.find("time")+4]=='=':
                data =line.split("time")[1].split("=")[1].split(" ")[0]
                delays.append(float(data))
    (mu,sigma) = norm.fit(delays)
    print mu, sigma

    outfile.write("Node %s, Mu: %f Sigma:%f\n"%(file.name.split(":")[0].split("/")[1],mu,sigma))

    #plt.plot(node,mu,"o")
    #plt.errorbar(node,mu,yerr=sigma,label=r"Node %d: $\mu=%3.f,\ \sigma=%.3f$"%(node,mu,sigma),fmt=".",barsabove=True)
    #plt.errorbar(distance,mu,yerr=sigma,label=r"Node %d: $\mu=%f,\ \sigma=%f$"%(node,mu,sigma),fmt=".",barsabove=True)
    distances_.append(distance)
    delays_.append(mu)
    sigmas_.append(sigma)

    # plt.xlabel("Nodes",fontsize=7,style="italic")
    # plt.ylabel("Delay (Ms)",fontsize=7,style="italic")
    # plt.title('Delay per node')
    # #plt.annotate(r"$\mu=%3.f,\ \sigma=%.3f$"%(mu,sigma),(node,mu+sigma))
    # plt.grid(True)
    # plt.tight_layout()
    # #plt.legend(title=
    # plt.legend(ncol=2,shadow=True,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize=10,numpoints=1)
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
        files=[]
        added=[]
        #pdb.set_trace()
        for directory in sys.argv[1:]:
            for fileinput in os.listdir(directory):
                #files.append((directory+"/"+fileinput,dst[fileinput.split(":")[0]]))
                if not fileinput.split("node")[0] in added or fileinput.find("Argentina")!=-1:
                    #print fileinput.split("node")[0]
                    distance_=0
                    added.append(fileinput.split("node")[0])
                    if fileinput.find("Spain")!= -1:
                        print fileinput.split("node")[0].split(":")[1]
                        distance_=distances[SpainNodes[fileinput.split("node")[0].split(":")[1]]]
                    else:
                        distance_ = distances[fileinput.split(":")[0]]
                    files.append((directory+"/"+fileinput,distance_))

        ordered_files=sorted(files, key= lambda file:file[1])
        outputfile=open("DelayClients.txt","w")
        print ordered_files
        for file in ordered_files:
            f = open(file[0],"r")
            #plot_delay(f,node)
            plot_delay(f,node,file[1],outputfile)
            node+=1
            #plt.show()

        for i in range(0,len(distances_)):
            plt.errorbar(distances_[i],delays_[i],yerr=sigmas_[i],fmt=".",barsabove=True,label="Node %d: $\mu=%f,\ \sigma=%f$"%(i,delays_[i],sigmas_[i]))

        plt.legend(ncol=2,shadow=True, loc=9, bbox_to_anchor=(0.5, -0.1),borderaxespad=0.,fontsize=10,numpoints=1)
        plt.xlabel("Distance (km)",fontsize=10,style="italic")
        plt.ylabel("Latency (ms)",fontsize=10,style="italic")
        #plt.title('Latency per node',fontsize=12)
        plt.xlim(xmin=0)
        plt.ylim(ymin=-200)
        y =( 0.0228*np.array(distances_)) + 17.88

        plt.plot(np.array(distances_),y,"b-")
        plt.autoscale(enable=True, axis='both', tight=False)

        savefig("DelayNodes"+".pdf",bbox_inches='tight',dpi=300)

    except IOError as e:
        print e
        if f:
            f.close()
        exit(-1)

    #f.close()
