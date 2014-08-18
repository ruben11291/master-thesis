#!/usr/bin/python
# -*- mode:python; coding:utf-8; tab-width:4 -*-

import sys

import Ice
Ice.loadSlice('-I {} cannon.ice'.format(Ice.getSliceDir()))
import Cannon
Ice.loadSlice('-I %s container.ice' % Ice.getSliceDir())
import Services

from matrix_utils import matrix_multiply, matrix_add


class ProcessorI(Cannon.Processor):
    row = None
    col = None
    above = None
    left = None
    order = None
    target = None
    current_step = None
    result_parcial = None
    A_blocks = []
    B_blocks = []

    def init(self, row, col, above, left, order, target, current=None):
        self.row=row
        self.col=col
        self.above=above
        self.left=left
        self.order=order
        self.target=target

        self.A_blocks = [None] * order
        self.B_blocks = [None] * order

        self.current_step = 0
        self.result_parcial = None

    def injectFirst(self, A, step, current=None):
        self.A_blocks[step] = A
        self.try_multiply()

    def injectSecond(self, B, step, current=None):
        self.B_blocks[step] = B
        self.try_multiply()

    def try_multiply(self):
        current_A = self.A_blocks[self.current_step]
        current_B = self.B_blocks[self.current_step]

        if current_A is None or current_B is None:
            return

        if self.current_step == 0:
            self.result_parcial = Cannon.Matrix(current_A.ncols, [0] * (current_A.ncols ** 2))

        product = matrix_multiply(current_A,current_B)
        self.result_parcial = matrix_add(self.result_parcial,product)
        self.current_step += 1

        if self.current_step == self.order:
            self.target.injectSubmatrix(self.result_parcial, self.row, self.col)
            return

        self.left.injectFirst(current_A, self.current_step)
        self.above.injectSecond(current_B, self.current_step)

        self.try_multiply()

class Server(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        servant = ProcessorI()

        adapter = broker.createObjectAdapter('ProcessorAdapter')
        proxy = adapter.addWithUUID(servant)

        proxyContainer = broker.stringToProxy(args[1])
        container = Services.ContainerPrx.checkedCast(proxyContainer)

        while not container:
            container = Services.ContainerPrx.checkedCast(proxyContainer)

        container.link(broker.identityToString(proxy.ice_getIdentity()), proxy)

        print('New processor ready: "{}"'.format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()
        container.unlink(broker.identityToString(proxy.ice_getIdentity()))


if __name__ == '__main__':
    app = Server()
    sys.exit(app.main(sys.argv))
