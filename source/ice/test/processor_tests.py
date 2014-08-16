#!/usr/bin/python
# -*- coding:utf-8; tab-width:4; mode:python -*-

from unittest import TestCase

from hamcrest import assert_that, anything
from doublex import Spy, Stub, called, ANY_ARG

import Ice
Ice.loadSlice('-I {} Geocloud.ice'.format(Ice.getSliceDir()))
import geocloud

from processor import ProcessorI

class ProcessorTests(TestCase):

    def test_processor_operations(self):
        P=ProcessorI()
        orchestrator = Spy(geocloud.Orchestrator)
        P.processImage("path_example")
        assert_that(orchestrator.imageProcessed, called().with_args("path_example"))
