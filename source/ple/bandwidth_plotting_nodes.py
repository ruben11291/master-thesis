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


distances_ = []
bandwidth_=[]
sigmas_=[]

#plt.set_figsize_inches(1024,872)
def plot_bandwith(file,node,distance,outfile):
    bandwith = []
    time = []
    for line in file:
        l = line.split(",")
        if len(l) == 9: #the it is a client report
            transfered=l[7]
            Bps=float(l[8])
            time_=l[6].split('-')[0]
            if (Bps > 0.0):
                bandwith.append(float(float(Bps)/1000))
                time.append(time_)
        else:
            #the server's report
            total_trans=l[7]
            average_bandwith=l[8]
            jitter=l[9]
            loss=l[10]
            total_pack=l[11]
            loss_rate =l[12]


    # print "Average ", average_bandwith, "SD ",sd
    #plt.xlabel("Time (s)")
    #plt.ylabel("Bandwith (Kb)")
    #plt.plot(time[:-1],bandwith[:-1],"r.",label="Bandwith")
    (mu,sigma) = norm.fit(bandwith[:-1])
    outfile.write("Node %s, Mu: %f Sigma:%f\n"%(file.name.split(":")[0].split("/")[1],float(mu),float(sigma)))
    distances_.append(distance)
    bandwidth_.append(float(mu/1000))
    sigmas_.append(float(sigma/1000))
    #plt.plot(node,mu,".")
    #print "D: ",distance
    #plt.plot(float(distance),float(mu),".")
    #plt.errorbar(distance,mu,yerr=sigma,label=r"Node %d: $\mu=%3.f,\ \sigma=%.3f$"%(node,mu,sigma),fmt=".",barsabove=True)


    #subplot.plot(bins,y,'b-')
   # subplot.subplots_adjust(left=0.15)
    #print file.name.split(":")[0].split("/")[1]
    #plt.xlabel("Distance (km)",fontsize=7,style="italic")
    #plt.ylabel("Bandwidth (Kbps)",fontsize=7,style="italic")
   # plt.title('Bandwidth per node')
    #plt.annotate(r"$\mu=%3.f,\ \sigma=%.3f$"%(mu,sigma),(node,mu+sigma))
    #plt.grid(True)
    #plt.tight_layout()
    #plt.legend(title=
    #plt.legend(ncol=2,shadow=True,bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.,fontsize=10,numpoints=1)
    #plt.set_figwidth(20)
    #plt.autoscale(enable=True, axis='both', tight=True)
#savefig(file.name.split(":")[0].split("/")[1]+"GS"+".png")
    #plt.show()
    # plt.xlim(xmin=-1)#x limits
   #  plt.xlim(xmax=node+1)
   #  plt.ylim(ymin=-10)
   # #
    #plt.ylim(ymin=mu-sigma-2)#y limit
    #plt.ylim(ymax=mu+sigma+2)

if __name__=="__main__":
    if len(sys.argv) < 2:
        print "Error with arguments. You must enter at least a file"
    try:

        node=1
        files=[]
        added=[]

        f_des=open("GSBandwidth.txt","w")
        for directory in sys.argv[1:]:
            for fileinput in os.listdir(directory):
                if not fileinput.split("node")[0] in added or fileinput.find("Argentina")!=-1:
                    distance_=0
                    added.append(fileinput.split("node")[0])
                    if fileinput.find("Spain")!= -1:
                        print fileinput.split("node")[0].split(":")[1]
                        distance_=distances[SpainNodes[fileinput.split("node")[0].split(":")[1]]]
                    else:
                        distance_ = distances[fileinput.split(":")[0]]
                    print fileinput
                    files.append((directory+"/"+fileinput,distance_))


        ordered_files=sorted(files, key= lambda file:file[1])
        for file in ordered_files:
            f = open(file[0],"r")
            plot_bandwith(f,node,file[1],f_des)
            node+=1

        plt.plot(np.array(distances_),np.array(bandwidth_),".")

        for i in range(0,len(distances_)):
            plt.errorbar(distances_[i],bandwidth_[i],yerr=sigmas_[i],fmt=".",barsabove=True,label="Node %d: $\mu=%f,\ \sigma=%f$"%(i,bandwidth_[i],sigmas_[i]))
        #plt.legend(ncol=2,shadow=True,bbox_to_anchor=(1.05, 1), loc=5, borderaxespad=0.,fontsize=7,numpoints=1)
        #figure(figsize=(12,9))
        #plt.legend(ncol=2,shadow=True, loc=1, borderaxespad=0.,fontsize=8,numpoints=1)bbox_to_anchor=(-0.5, -.2)
        plt.legend(ncol=2,shadow=True, loc=9, bbox_to_anchor=(0.5, -0.1),borderaxespad=0.,fontsize=10,numpoints=1)
        plt.xlabel("Distance (km)",fontsize=10,style="italic")
        plt.ylabel("Bandwidth (Mbps)",fontsize=10,style="italic")
        #plt.title('Bandwidth per node',fontsize=12)

        y =( 18.491 * (np.array(distances_)**(-0.547)))*10

        plt.plot(np.array(distances_),y,"b-")
        plt.autoscale(enable=True, axis='both', tight=False)
        savefig("GSNodes"+".pdf",bbox_inches='tight',dpi=500,papertype='a4',orientation='landscape',figsize=(300,200))

    except IOError as e:
        print e
        if f:
            f.close()
        exit(-1)

    f.close()
