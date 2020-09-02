import skrf as rf
ntwk = rf.Network('FEM_POUT.S1P')
ntwk.frequency.unit = 'mhz'
#ntwk.frequency.span = 30
#ntwk.frequency.stop = 930

ntwk.plot_s_db()
#ntwk.plot_s_smith()