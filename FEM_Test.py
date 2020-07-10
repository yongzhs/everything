# written for Skyworks SE2435L evaluation board...
TRANSMIT_VS_LEVEL = False
TRANSMIT_VS_FREQ = True
RECEIVE_TEST_VS_LEVEL = False # gain vs level
RECEIVE_VS_FREQ = False

import spectrum_Analyzer, signal_Generator, time, power_Supply
import matplotlib.pyplot as plt
sa = spectrum_Analyzer.spectrum_Analyzer('172.17.213.116')   # spectrum analyzer, please set up spectrum analyzer manually before the script
sg = signal_Generator.signal_Generator('172.17.213.17')    # signal generator
# ps = power_Supply.power_Supply('ASRL19::INSTR')             # power supply

# in this test, subplot 1: pout vs pin; subplot 2: Icc vs Pin; subplot 3: gain vs pout; subplot 4: PAE vs pout
# if TRANSMIT_VS_LEVEL:
#     p_num = 29
#     pin = [-22 + i for i in range(p_num)]
#     pout = [0 for i in range(p_num)]
#     c = [0 for i in range(p_num)]           # store current data here
#     gain = [0 for i in range(p_num)]        # store gain data here
#     pae = [0 for i in range(p_num)]         # store PAE data here
#     sg.setFreq(915e6)                       # test frequency is 915MHz
#     sa.setCenterFreq(915e6)
#     sg.rfOn(True)
#     for i in range(p_num):
#         sg.setPower(pin[i])
#         time.sleep(0.1)
#         sa.setPeakSearch()
#         pout[i] = sa.getMarkerY()
#         c[i] = float(ps.getCurrent()) * 1000
#         gain[i] = pout[i] - pin[i]
#         pae[i] = 10**(pout[i] / 10) / c[i] * 25
#     sg.rfOn(False)
#
#     plt.subplot(221)
#     plt.plot(pin, pout)
#     plt.xlabel('Input power (dBm)')
#     plt.ylabel('Pout (dBm)')
#     plt.grid()
#
#     plt.subplot(222)
#     plt.plot(pin, c)
#     plt.xlabel('Input power (dBm)')
#     plt.ylabel('Icc (mA)')
#     plt.grid()
#
#     plt.subplot(223)
#     plt.plot(pout, gain)
#     plt.xlabel('Output power (dBm)')
#     plt.ylabel('Gain (dB)')
#     plt.grid()
#
#     plt.subplot(224)
#     plt.plot(pout, pae)
#     plt.xlabel('Output power (dBm)')
#     plt.ylabel('PAE (%)')
#     plt.grid()

# this section find gain vs frequency at -10dBm input power
if TRANSMIT_VS_FREQ:
    f_num = 200
    sg.setPower(-10)
    sg.rfOn(True)
    f = [500 + 5 * (i + 1) for i in range(f_num)]
    pout_f = [0 for i in range(f_num)]
    gain_f = [0 for i in range(f_num)]
    for i in range(f_num):
        sg.setFreq(f[i] * 1e6)
        sa.setCenterFreq(f[i] * 1e6)
        time.sleep(0.1)
        sa.setPeakSearch()
        pout_f[i] = sa.getMarkerY()
        gain_f[i] = pout_f[i] + 10
    sg.rfOn(False)
    
    plt.plot(f, gain_f)
    plt.xlabel('Frequency (MHz)')
    plt.ylabel('Gain (dB)')
    plt.title('Gain vs frequency at -10dBm input')
    plt.grid()

# this section plots LNA gain vs different input power at 915MHz
# if RECEIVE_TEST_VS_LEVEL:
#     p_num = 20
#     pin = [-25 + i for i in range(p_num)]
#     pout = [0 for i in range(p_num)]
#     c = [0 for i in range(p_num)]           # store current data here
#     gain = [0 for i in range(p_num)]        # store gain data here
#     sg.setFreq(915e6)                       # test frequency is 915MHz
#     sa.setCenterFreq(915e6)
#     sg.rfOn(True)
#     for i in range(p_num):
#         sg.setPower(pin[i])
#         time.sleep(0.1)
#         sa.setPeakSearch()
#         pout[i] = sa.getMarkerY()
#         c[i] = float(ps.getCurrent()) * 1000
#         gain[i] = pout[i] - pin[i]
#     sg.rfOn(False)
#
#     plt.subplot(311)
#     plt.plot(pin, pout)
#     plt.xlabel('Input power (dBm)')
#     plt.ylabel('Pout (dBm)')
#     plt.grid()
#
#     plt.subplot(312)
#     plt.plot(pin, c)
#     plt.xlabel('Input power (dBm)')
#     plt.ylabel('Icc (mA)')
#     plt.grid()
#
#     plt.subplot(313)
#     plt.plot(pout, gain)
#     plt.xlabel('Output power (dBm)')
#     plt.ylabel('Gain (dB)')
#     plt.grid()

# this section find gain vs frequency at -20dBm input power
# if RECEIVE_VS_FREQ:
#     f_num = 31
#     sg.setPower(-20)
#     sg.rfOn(True)
#     f = [i + 900 for i in range(f_num)]
#     pout_f = [0 for i in range(f_num)]
#     gain_f = [0 for i in range(f_num)]
#     for i in range(f_num):
#         sg.setFreq(f[i] * 1e6)
#         sa.setCenterFreq(f[i] * 1e6)
#         time.sleep(0.1)
#         sa.setPeakSearch()
#         pout_f[i] = sa.getMarkerY()
#         gain_f[i] = pout_f[i] + 10
#     sg.rfOn(False)
#
#     plt.plot(f, gain_f)
#     plt.xlabel('Frequency (MHz)')
#     plt.ylabel('Gain (dB)')
#     plt.title('Gain vs frequency at -20dBm input')
#     plt.grid()