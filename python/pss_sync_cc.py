#!/usr/bin/env python
# -*- coding: utf-8 -*-
#                     GNU GENERAL PUBLIC LICENSE
#                        Version 3, 29 June 2007


import numpy
from gnuradio import gr
from nrphypy import decode
from collections import deque

class pss_sync_cc(gr.basic_block):
    """
    docstring for block pss_sync_cc
    """

    def __init__(self, fft_size, threshold, L_max):
        gr.basic_block.__init__(self,
                                name="pss_sync_cc",
                                in_sig=[(numpy.complex64, (1,))],
                                # nid2, ssb
                                out_sig=[(numpy.int32, (1,)), (numpy.complex64, 240*4)])
        self.fft_size = fft_size
        self.threshold = threshold
        self.L_max = L_max
        self.memory = numpy.array([],dtype=complex)
        self.ssb = deque([],maxlen=self.L_max)
        self.can_pss_t = decode._pss_candidates(self.fft_size)

    def forecast(self, noutput_items, ninputs):
        ninput_items_required = [self.fft_size]*ninputs #[self.fft_size*4]*ninputs
        # setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items
        return ninput_items_required

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        self.memory = numpy.concatenate((self.memory, in0.flatten().copy()))
        self.consume_each(len(in0))

        if len(self.memory) >= self.fft_size*4 and not len(self.ssb) == self.ssb.maxlen:
            grids, nids, proc_samples, _ = decode.sync_pss(received_data= self.memory,fft_size= self.fft_size, threshold= self.threshold,pss_candidates= self.can_pss_t)
            self.memory = self.memory[proc_samples:]
            for i in range(len(grids)):
                self.ssb.append([grids[i], nids[i]])


        n_out_items = min(len(output_items[1]), len(self.ssb))
        for i in range(n_out_items):
            ssb, nid2 = self.ssb.popleft()
            output_items[0][i][0] = nid2
            output_items[1][i][:] = ssb.flatten(order='F')
        
        return n_out_items
