#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2021 Mark Disterhof.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy
from gnuradio import gr
from nrphypy import ssb

class unmap_ssb_cc(gr.sync_block):
    """
    docstring for block unmap_ssb_cc
    """

    def __init__(self, nu):
        gr.sync_block.__init__(self,
                               name="unmap_ssb_cc",
                               in_sig=[(numpy.complex64, 4*240),
                                       (numpy.int32, (1,))],
                               out_sig=[
                                   (numpy.complex64, 127),  # sss
                                   (numpy.complex64, 432),  # pbch
                                   ((numpy.int32, (1,))),  # i_ssb
                                   (numpy.complex64, 144)])  # dmrs
        self.nu = nu

    def work(self, input_items, output_items):
        in0 = input_items[0]        
        in1 = input_items[1]
        out0 = output_items[0]
        out1 = output_items[1]
        out2 = output_items[2]
        out3 = output_items[3]

        for i in range(len(in0)):
            grid = numpy.array(in0[i], dtype=complex).reshape(
                (240, 4), order='F')
            
            # <+signal processing here+>
            sss_data = ssb.unmap_sss(grid)
            pbch_data, dmrs_data = ssb.unmap_pbch(grid, self.nu)
            out0[i] = sss_data
            out1[i] = pbch_data
            out2[i] = in1[i]
            out3[i] = dmrs_data
        return len(out0)
