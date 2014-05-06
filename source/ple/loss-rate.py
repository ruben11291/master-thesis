#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-
"""This script makes a plot representing the bandwith of a node in front of the time"""


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
#mpl.rcParams['font.size']=7
#mpl.rcParams['axes.xmargin']=2
#mpl.rcParams['axes.ymargin']=2
mpl.rcParams['figure.subplot.wspace']=0.4
mpl.rcParams['figure.subplot.hspace']=0.4
mpl.rcParams['figure.subplot.bottom']=0.0
mpl.rcParams['savefig.bbox']='tight'

loss_rate_ = []
node_ =[]

#plt.set_figsize_inches(1024,872)
def plot_loss_rate_gs(file,node,distance,outfile):
    num=0
    for line in file:
        if line.find("%") != -1:
            num = (line[line.find("(")+1:line.find("%")])

    node_.append(int(node))
    loss_rate_.append(float(num))


def plot_loss_rate_customers(file,node,distance,outfile):
    loss_rate=0
    for line in file:
        l = line.split(",")
        #print len(l)
        if len(l) == 14:
            loss_rate = float(l[-4])/float(l[-3])
            #print loss_rate
    loss_rate_.append(float(loss_rate)*100)
    node_.append(int(node))

if __name__=="__main__":
    if len(sys.argv) < 2:
        print "Error with arguments. You must enter at least a file"
    try:
        #pdb.set_trace()
        output=open("GSLoss-rate.txt","w")
        files=[]
        added=[]

        for fileinput in os.listdir(os.sys.argv[1]):
            print fileinput
            if not fileinput.split("node")[0] in added or fileinput.find("Argentina")!=-1:

               # files.append((os.sys.argv[1]+"/"+fileinput,distances[fileinput.split(":")[0]],plot_loss_rate_gs))
                distance_=0
                added.append(fileinput.split("node")[0])
                if fileinput.find("Spain")!= -1:
                    print fileinput.split("node")[0].split(":")[1]
                    distance_=distances[SpainNodes[fileinput.split("node")[0].split(":")[1]]]
                else:
                    distance_ = distances[fileinput.split(":")[0]]
                files.append((os.sys.argv[1]+"/"+fileinput,distance_,plot_loss_rate_gs))

            #f = open(os.sys.argv[1]+"/"+fileinput,"r")
            #plot_loss_rate_gs(f,node,output)
        for fileinput in os.listdir(os.sys.argv[2]):
            print fileinput
            if not fileinput.split("node")[0] in added or fileinput.find("Argentina")!=-1:

                # files.append((os.sys.argv[1]+"/"+fileinput,distances[fileinput.split(":")[0]],plot_loss_rate_gs))
                distance_=0
                added.append(fileinput.split("node")[0])
                if fileinput.find("Spain")!= -1:
                    print fileinput.split("node")[0].split(":")[1]
                    distance_=distances[SpainNodes[fileinput.split("node")[0].split(":")[1]]]
                else:
                    distance_ = distances[fileinput.split(":")[0]]
                files.append((os.sys.argv[2]+"/"+fileinput,distance_,plot_loss_rate_customers))
            #files.append((os.sys.argv[2]+"/"+fileinput,distances[fileinput.split(":")[0]],plot_loss_rate_customers))

            #f = open(os.sys.argv[2]+"/"+fileinput,"r")
            #plot_loss_rate_customers(f,node,output)
        #plt.show()
        ordered_files=sorted(files, key= lambda file:file[1])

        node=1

        for file in ordered_files:
            print file
            f = open(file[0],"r")
            #plot_delay(f,node)
            file[2](f,node,file[1],output)
            node+=1

        def autolabel(rects):
            for rect in rects:
                h = rect.get_height()
                plt.text(rect.get_x()+rect.get_width()/2., 1.05*h, '    %.3f'%float(h),
                        ha='center', va='bottom',rotation='vertical')

        fig=plt.figure(figsize=(20,19))

        # Set color transparency (0: transparent; 1: solid)
        a = 0.7
# Create a colormap
        customcmap = [(x/50.,  x/40., 0.05) for x in range(len(loss_rate_))]
        print customcmap
        for i in range(0,len(loss_rate_)):
            print node_[i],loss_rate_[i]
            if loss_rate_[i] < 10:
                print loss_rate_[i]
                color=float(node)/len(loss_rate_)
                print color
                r=plt.bar(node_[i],loss_rate_[i],label="Node %d"%(i),color=customcmap[i])
                autolabel(r)

        #plt.bar(node_,loss_rate_)
        #plt.autoscale(enable=True, axis='both', tight=True)
        plt.legend(ncol=2,shadow=True, loc=9, bbox_to_anchor=(0.5, -0.1),borderaxespad=0.,fontsize=10,numpoints=1)

        #plt.show()

        savefig("Loss-rateALL"+".png",bbox_inches='tight',dpi=300)

    except IOError as e:
        print e
        if f:
            f.close()
        exit(-1)

    f.close()
