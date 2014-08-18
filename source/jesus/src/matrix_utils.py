# -*- mode:python; coding:utf-8; tab-width:4 -*-

import itertools
import math

import Ice
Ice.loadSlice('-I {} /tmp/DistributedSystem_grid/src/cannon.ice'.format(Ice.getSliceDir()))
import Cannon


def matrix_multiply(A, B):
    order = A.ncols
    C = Cannon.Matrix(order, [])

    for row in range(0, order):
        for col in range(0, order):
            result = 0
            for i in range(0, order):
                result += A.data[row*order+i] * B.data[i*order+col]
            C.data.append(result)

    return C


def matrix_add(A, B):
    order = A.ncols
    C = Cannon.Matrix(order, [])

    for pos in range(0, order**2):
            C.data.append(A.data[pos] + B.data[pos])

    return C


def matrix_horizontal_shift(M, block_order):
    order = M.ncols
    retval = Cannon.Matrix(order, [])

    for row in range(0, order):
        for col in range(0, order):
            step = block_order * int(row/block_order)
            retval.data.append(M.data[((col+step)%order)+row*order])   

    return retval


def matrix_vertical_shift(M, block_order):
    order = M.ncols
    retval = Cannon.Matrix(order, [])

    for row in range(0, order):
        for col in range(0, order):
            step = block_order * int(col/block_order)
            retval.data.append(M.data[((row+step)%order)*order+col])
     
    return retval


def matrix_split(M, block_order):
    blocks = []

    order = M.ncols
    blocks_row = int(order / block_order)
    nblocks = blocks_row ** 2
    
    for n_block in range(0, nblocks):
        blocks.insert(n_block, Cannon.Matrix(block_order, []))

    for row in range(0, order):
        for col in range(0, order):
            n_block = int(row/block_order) * int(blocks_row) + int(col/block_order)
            blocks[n_block].data.append(M.data[row*order+col])

    return blocks


def matrix_join(*blocks):
    nblocks = len(blocks)
    block_order = blocks[0].ncols
    order = int(math.sqrt(nblocks)) * block_order
    retval = Cannon.Matrix(order, [])

    for row in range(0, order):
        for col in range(0, order):
            n_block = int(row/block_order) * int(order/block_order) + int(col/block_order)
            block_pos = row%block_order * block_order + col%block_order         
            retval.data.append(blocks[n_block].data[block_pos])

    return retval


def load_matrix_from_file(filename):
    with file(filename) as f:
        rows = f.readlines()

    order = len(rows[0].split())
    retval = Cannon.Matrix(order, [])

    for row in rows:
        rowdata = row.split()
        assert len(rowdata) == order
        for n in rowdata:
            retval.data.append(float(n))

    assert len(retval.data) == order ** 2
    return retval


def save_matrix_to_file(m, filename):
    with file(filename, 'wt') as fd:
        for i, x in enumerate(m.data):
            fd.write("%s " % x)
            if (i + 1) % m.ncols == 0:
                fd.write('\n')

def list_split(M, block_order):
    matrix_aux = [0] * (len(M)/block_order)
    aux = 0
    size_matrix = len(matrix_aux)
    for i in range (0, size_matrix):
        matrix_aux[i] = M[aux:aux+block_order]
        aux+=block_order
    return matrix_aux