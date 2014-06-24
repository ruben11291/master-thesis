#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-
__doc__ = "usage: {0} <loader-proxy> <index>"

import sys

import Ice
Ice.loadSlice('-I {} cannon.ice'.format(Ice.getSliceDir()))
import Cannon

from matrix_utils import load_matrix_from_file


class Client(Ice.Application):
    def run(self, args):
        loader = self.string_to_proxy(args[1], Cannon.OperationsPrx)

        example = args[2]

        A = load_matrix_from_file('m/{}A'.format(example))
        B = load_matrix_from_file('m/{}B'.format(example))

        C = loader.matrixMultiply(A, B)

        expected = load_matrix_from_file('m/{}C'.format(example))

        retval = (C == expected)
        print("OK" if retval else "FAIL")
        return not retval

    def string_to_proxy(self, str_proxy, iface):
        proxy = self.communicator().stringToProxy(str_proxy)
        retval = iface.checkedCast(proxy)
        if not retval:
            raise RuntimeError('Invalid proxy %s' % str_proxy)

        return retval

    def print_matrix(self, M):
        ncols = M.ncols
        nrows = len(M.data) / ncols

        for r in range(nrows):
            print M.data[r * ncols:(r + 1) * ncols]


if __name__ == '__main__':
    # if len(sys.argv) != 2:
    #     print __doc__.format(__file__)
    #     sys.exit(1)

    sys.exit(Client().main(sys.argv))
