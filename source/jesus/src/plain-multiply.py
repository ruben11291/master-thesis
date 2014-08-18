#!/usr/bin/env python
# -*- mode:python; coding:utf-8; tab-width:4 -*-

__doc__ = "usage: ./multiply.py A B C"

import sys

from matrix_utils import matrix_multiply, load_matrix_from_file, save_matrix_to_file

a = load_matrix_from_file(sys.argv[1])
b = load_matrix_from_file(sys.argv[2])

c = matrix_multiply(a, b)

save_matrix_to_file(c, sys.argv[3])
