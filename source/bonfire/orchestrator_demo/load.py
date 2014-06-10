#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

import psutil
import os
class CpuStat:

    User = 0
    Nice = 1
    System = 2
    Idle = 3
    counter = 0


    def lookup(self):
        mycputimes=psutil.cpu_times(percpu=False)
        if os.name == "nt":
            tmp = [mycputimes.user,0.0,mycputimes.system,mycputimes.idle,0.0,0.0,0.0]
        else:
            tmp = [mycputimes.user,mycputimes.nice,mycputimes.system,mycputimes.idle,mycputimes.iowait,mycputimes.irq,mycputimes.softirq]
        return tmp

if __name__=="__main__":
    a = CpuStat()
    print a.lookup()
