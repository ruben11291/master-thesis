import sys, traceback, Ice,IceGrid

import geocloud
import sys,time

status = 0
ic = None
try:
    ic = Ice.initialize(sys.argv)
    base = ic.stringToProxy("broker")
    printer = geocloud.BrokerPrx.checkedCast(base)
    orches = geocloud.OrchestratorPrx.checkedCast(ic.stringToProxy("orchestrator"))
    ayc =  geocloud.ArchiveAndCataloguePrx.checkedCast(ic.stringToProxy("ayc"))

    if not printer:
        raise RuntimeError("Invalid proxy")

    printer.startScenario(1)
    # # s=printer.getLastLogs()
    # # print orches
    orches.downloadedImage("/home/deimos/TrueMarble.32km.1350x675.tif")
    orches.downloadedImage("/home/deimos/TrueMarble.32km.1350x675.tif")
    orches.downloadedImage("/home/deimos/TrueMarble.32km.1350x675.tif")
    orches.downloadedImage("/home/deimos/TrueMarble.32km.1350x675.tif")
    orches.downloadedImage("/home/deimos/TrueMarble.32km.1350x675.tif")

    # #time.sleep(1.0)
    # orches.downloadedImage('Segunda')
    # # #time.sleep(1.0)
    # orches.downloadedImage('Tercera')
    # # #time.sleep(1.0)
    # orches.downloadedImage('Cuarta')
    # # #time.sleep(1.0)
    # orches.downloadedImage("quinta")
    # orches.downloadedImage("sexta")
    # orches.downloadedImage("sexta1")
    # orches.downloadedImage("sexta2")

    # printer.begin_stopScenario(1)
    # orches.imageProcessed("cam")
    # orches.imageProcessed("c   ")
    # orches.imageProcessed("b  ")
    # orches.imageProcessed("4")
    # orches.imageProcessed("e  ")
    # orches.imageProcessed("r")
    # ayc.createScenario("2")
    # ayc.catalogue("/home/deimos/TrueMarble.32km.1350x675.tif","TrueMarble","2")

    s=printer.getLastLogs()
    print s
except:
    traceback.print_exc()
    status = 1

if ic:
    # Clean up
    try:
        ic.destroy()
    except:
        traceback.print_exc()
        status = 1

sys.exit(status)
