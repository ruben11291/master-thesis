 #!/usr/bin/env python

import threading
import pdb
from processingChain import processingChainController
from AyC import catalog
import xml.dom.minidom

class Iorchestator:
    def setImage(self,img):
        None
    

class orchestator(Iorchestator):

    def __init__(self):
        self._geoserver_path = ""
        self._service_pp = ""
        self._database_ip = ""
        self.ftp_user=""
        self.ftp_passwd=""
        try:
            get_info()
        except IOError:
            print "Error with xml config file!"
            exit(0)
        print "[Orchestrator] Creating orchestrator!"
        controller = processingChainController.get()
        controller.setOrchestrator(self)
        
        self.catalog = catalog.catalog("http://localhost:8080/geoserver/rest")
        print "[Orchestrator] Initializing geoserver client"
        self.i = 0
        print "[Orchestrator] Initializing processing chaing controller!"

    def processRawData(self,img):
        print "[Orchestrator] Creating processing chain!"
        controller = processingChainController.get()
        controller.createProcessingChain(img)
        
    def processedRawData(self,fileOutput):
        #eviar a espacio compartido y donde tiene el working directory geoserver
        None
        #print "[Orchestrator] Processed raw data!"
        #self.sendToCatalog(fileOutput)

    # def sendToCatalog(self, data):
    #     self.i = self.i +1
    #     wksp = None
    #    # pdb.set_trace()
    #     while True:
    #         try:
    #             wksp = self.catalog.createWkspace("Escen"+str(self.i))
    #             break
    #         except Exception:
    #             self.i = self.i+1
    #     print data
    #     self.catalog.addImage(str(self.i),wksp,data)
        

    def sendToStore(self):
        None
        
    def get_info(self, geoserver, pp, database):
        
        file = xml.dom.minidom.parse("orchestrator.conf.xml")
        nodes = file.childNodes
        self.ftp_user = nodes[0].getElementsByTagName("ftp")[0].getElementsByTagName("user")[0].firstChild.toxml()
        self.ftp_pass = nodes[0].getElementsByTagName("ftp")[0].getElementsByTagName("passwd")[0].firstChild.toxml()
        self._geoserver_path = nodes[0].getElementsByTagName("address")[0].getElementsByTagName("geoserver_path")[0].firstChild.toxml()
        self._database_ip = nodes[0].getElementsByTagName("address")[0].getElementsByTagName("database")[0].firstChild.toxml()
        self._service_ip=nodes[0].getElementsByTagName("address")[0].getElementsByTagName("pp_service")[0].firstChild.toxml()

    
