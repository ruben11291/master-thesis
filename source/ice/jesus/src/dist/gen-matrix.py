#!/usr/bin/env python
# -*- mode:python; coding:utf-8; tab-width:4 -*-

__doc__ = "usage: ./gen-matrix.py <file> <first> <order>"

import sys

import Ice
Ice.loadSlice('-I {} cannon.ice'.format(Ice.getSliceDir()))
import Cannon

from matrix_utils import save_matrix_to_file

out = sys.argv[1]
ini = int(sys.argv[2])
order = int(sys.argv[3])


def gen_matrix(ini, order):
    return Cannon.Matrix(order, xrange(ini, ini + order ** 2))

save_matrix_to_file(gen_matrix(ini, order), out)
