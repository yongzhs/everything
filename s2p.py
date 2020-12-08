import skrf as rf
ntwk = rf.Network('HW4.2_S2P_from_brd_to_flex_ant.S2P')
ntwk.frequency.unit = 'mhz'
#ntwk.frequency.span = 30
#ntwk.frequency.stop = 930

ntwk.plot_s_db()
#ntwk.plot_s_smith()