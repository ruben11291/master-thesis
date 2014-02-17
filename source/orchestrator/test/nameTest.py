#!/usr/bin/env python

import os
import time
import unittest

def processingName(name):
    sp = name.split('_')
    readwrite = sp[0]
    idGs = sp[1]
    hour = sp[2]
    date = sp[3]
    return [readwrite,idGs,hour,date]

def createNameFile(idGs, date, readwrite):
    return readwrite+"_"+idGs+"_"+str(date.tm_hour)+":"+str(date.tm_min)+":"+str(date.tm_sec)+"_"+str(date.tm_mday)+"/"+str(date.tm_mon)+"/"+str(date.tm_year)


class TestprocessingDateTest(unittest.TestCase):
    
    def test_createNameFile(self):
        t = time.localtime(12333313.03)
        f = createNameFile("GS12",t,"W")
        self.assertTrue(f == "W_GS12_18:55:13_23/5/1970")

        t = time.localtime(1112288888.03)
        f = createNameFile("GS01",t, "R")
        self.assertTrue(f == "R_GS01_19:8:8_31/3/2005")

    def test_processingName(self):
        t = time.localtime(12333313.03)
        f = createNameFile("GS12",t,"W")
        res = processingName(f)
        self.assertTrue(res[0] == "W")
        self.assertTrue(res[1] == "GS12")
        self.assertTrue(res[2] == "18:55:13")
        self.assertTrue(res[3] == "23/5/1970")

        t = time.localtime(1112288888.03)
        f = createNameFile("GS01",t,"R")
        res = processingName(f)
        self.assertTrue(res[0] == "R")
        self.assertTrue(res[1] == "GS01")
        self.assertTrue(res[2] == "19:8:8")
        self.assertTrue(res[3] == "31/3/2005")

if __name__=='__main__':
    unittest.main()
