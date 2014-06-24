#!/usr/bin/python
# -*- mode:python; coding:utf-8; tab-width:4 -*-

import sys
import math

import Ice
Ice.loadSlice('-I {} cannon.ice'.format(Ice.getSliceDir()))
import Cannon
Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())
import Services
import threading

from matrix_utils import matrix_horizontal_shift, matrix_vertical_shift, matrix_split, matrix_join


class OperationsI(Cannon.Operations):
	processors = None
	nprocs = None
    order = None
    collector = None
    adapter = None
    proxy = None

    def __init__(self, processors):
        self.processors = processors
        self.nprocs = len(self.processors)
        self.order = int(math.sqrt(self.nprocs))

    def matrixMultiply(self, A, B, current=None):
        self.adapter = current.adapter
        self.create_collector()


        self.init_processors()
        self.load_processors(A, B)
        
        retval = self.wait_for_result()

        self.destroy_collector()

        return retval

    def create_collector(self):
        self.collector = CollectorI(self.order)
        self.proxy = Cannon.CollectorPrx.checkedCast(self.adapter.addWithUUID(self.collector))

    def destroy_collector(self):
        self.adapter.remove(self.proxy.ice_getIdentity())
        del(self.collector)

    def init_processors(self):
        row = None
        col = None

        for i in range(self.nprocs):
            row = i / self.order
            col = i % self.order

            above = i - self.order
            if row==0:
            	above += self.order ** 2

            left = i- 1
            if col==0:
            	left += self.order

            self.processors[i].init(row,col,self.processors[above],self.processors[left],self.order,self.proxy)
    
    def load_processors(self, A, B):
        nblocks = self.nprocs
        block_order = int(A.ncols/self.order)

        A_shift = matrix_horizontal_shift(A,block_order)
        B_shift = matrix_vertical_shift(B,block_order)

        A_blocks = matrix_split(A_shift,block_order)
        B_blocks = matrix_split(B_shift,block_order)

        for i in range (nblocks):
        	self.processors[i].injectFirst(A_blocks[i], 0)
        	self.processors[i].injectSecond(B_blocks[i], 0)

    def wait_for_result(self):
        return self.collector.get_result()

class CollectorI(Cannon.Collector):
    blocks = []
    block_order = None
    order = None
    received_nblocks = None
    event = None
    
    def __init__(self, order):
        self.blocks = [None] * (order**2)
        self.order = order
        self.received_nblocks = 0
        self.block_order = order
        self.evento = threading.Event()
        
    def injectSubmatrix(self, block, row, col, current=None):
        self.blocks[self.block_order*row+col] = block   
        self.received_nblocks += 1
        if (self.received_nblocks == (self.order ** 2)):
			self.evento.set()
        
    def get_result(self):
        if(self.evento.wait(5)):
            return matrix_join(*self.blocks)
        else:
            return None

class Server(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        proc = []

        adapter = broker.createObjectAdapter('LoaderAdapter')

		proxyContainer = broker.stringToProxy(args[1])
		container = Services.ContainerPrx.checkedCast(proxyContainer)

		if not container:
            raise RuntimeError('Invalid proxy')

		for processor in container.list().values():
			try:
				processor.ice_ids()
			    print "processor", processor, "OK"
			except Ice.ObjectNotExistException:
				print processor, "does not exist"
				continue			
			proc.append(Cannon.ProcessorPrx.checkedCast(processor))

        servant = OperationsI(proc)

        proxy = adapter.add(servant, broker.stringToIdentity("loader1"))

        print('loader ready: "{}"'.format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
    	

if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
