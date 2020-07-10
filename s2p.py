# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 12:42:51 2019

@author: yshao
"""
import skrf as rf
ntwk = rf.Network('brd3238_old12s.s2p')
ntwk.frequency.unit = 'mhz'
#ntwk.frequency.span = 30
#ntwk.frequency.stop = 930

ntwk.plot_s_db()
#ntwk.plot_s_smith()