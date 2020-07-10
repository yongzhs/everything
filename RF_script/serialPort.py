import datetime
import math
import time
import RF_PHY
import serial
import xlsxwriter
from PyQt5.QtCore import QThread


class serialPort:  # this class is interface between GUI and RF_PHY api...
    def __init__(self):
        self.m_serialPort = serial.Serial()  # Get a Serial instance and configure/open it later

    def __del__(self):  # destructor closes the port on closing if port is open
        if self.m_serialPort.is_open:
            self.m_serialPort.close()
        del self.m_serialPort

    def slot_openUart(self, m_mainWindow):
        try:
            self.m_serialPort = serial.Serial(m_mainWindow.m_port.currentText(), 115200, timeout=0)
            print("Connected to " + m_mainWindow.m_port.currentText())
            m_mainWindow.m_connectPort.setEnabled(False)
            m_mainWindow.m_disconnectPort.setEnabled(True)
            m_mainWindow.m_txStart.setEnabled(True)
            m_mainWindow.m_txStop.setEnabled(True)
            m_mainWindow.m_txACLR.setEnabled(True)
            m_mainWindow.m_rxConfig.setEnabled(True)
            m_mainWindow.m_rssiRequest.setEnabled(True)
            m_mainWindow.m_sensitivity.setEnabled(True)
            m_mainWindow.m_rssiSweep.setEnabled(True)
            self.thread = parse(m_mainWindow)
            self.thread.start()
        except:
            print("Error!?")

    def slot_closeUart(self, m_mainWindow):
        try:
            self.m_serialPort.close()
            print("Disconnected from " + m_mainWindow.m_port.currentText())
            m_mainWindow.m_connectPort.setEnabled(True)
            m_mainWindow.m_disconnectPort.setEnabled(False)
            m_mainWindow.m_txStart.setEnabled(False)
            m_mainWindow.m_txStop.setEnabled(False)
            m_mainWindow.m_txACLR.setEnabled(False)
            m_mainWindow.m_rxConfig.setEnabled(False)
            m_mainWindow.m_rssiRequest.setEnabled(False)
            m_mainWindow.m_sensitivity.setEnabled(False)
            m_mainWindow.m_rssiSweep.setEnabled(False)
            self.thread.terminate()
        except:
            print("Error!")

    def slot_listPorts(self, m_mainWindow):  # the function lists all available ports
        ports = ['COM%s' % (i + 3) for i in
                 range(100)]  # https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python
        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        i = 0
        m_mainWindow.m_port.clear()
        for x in result:
            m_mainWindow.m_port.insertItem(i, x)
            i += 1

    def write(self, packet):
        self.m_serialPort.write(packet)

    def read(self):  # convert bytes to list
        data_t = (self.m_serialPort.read(1024))
        data_len = len(data_t)
        data = [0 for i in range(data_len)]
        for i in range(data_len):
            data[i] = data_t[i]
        return data


    def slot_startTx(self, m_mainWindow, m_sa):
        (mod, psdu, f, p, pkt_intval, numOfPacket) = self.get_txParameters(m_mainWindow)
        if m_mainWindow.m_testMode.isChecked():  # test mode
            (tx_attn_manual, tx_attn_rfic, tx_attn_digital, txContinuousMode, txCWMode,
             ant) = self.get_txTestModeParameters(m_mainWindow)
            if m_mainWindow.m_txLoopEnable.isChecked():  # loop Tx test mode
                f_stop = int(float(m_mainWindow.m_txFreqStop.text()) * 1000)
                f_step = int(float(m_mainWindow.m_txFreqStep.text()) * 1000)
                if (f_stop - f) % f_step == 0:
                    f_stop = f_stop + f_step  # add another step to f_stop because range does not include upper limit
                f_num = math.ceil((f_stop - f) / f_step)
                p_stop = m_mainWindow.m_txPowerStop.currentIndex()
                p_step = 1 << (m_mainWindow.m_txPowerStep.currentIndex())
                if (p_stop - p) % p_step == 0:
                    p_stop = p_stop + p_step
                p_num = math.ceil((p_stop - p) / p_step)
                f_count = 0

                timestamp = datetime.datetime.now().strftime("%m_%d_%H_%M")
                wb = xlsxwriter.Workbook('tx_power_sweep_' + timestamp + '.xlsx')
                sheet1 = wb.add_worksheet('Power')
                f_xls = f
                for i in range(f_num):
                    sheet1.write(i + 1, 0, f_xls)
                    f_xls = f_xls + f_step
                p_xls = p
                for i in range(p_num):
                    sheet1.write(0, i + 1, float(p_xls * 0.5))
                    p_xls = p_xls + p_step
                if m_mainWindow.m_txFreqOffsetEnable.isChecked():
                    sheet2 = wb.add_worksheet('ppm')
                    f_xls = f
                    for i in range(f_num):
                        sheet2.write(i + 1, 0, f_xls)
                        f_xls = f_xls + f_step
                    p_xls = p
                    for i in range(p_num):
                        sheet2.write(0, i + 1, float(p_xls * 0.5))
                        p_xls = p_xls + p_step
                for f1 in range(f, f_stop, f_step):
                    p_count = 0
                    for p1 in range(p, p_stop, p_step):
                        m_sa.setCenterFreq(f1 * 1000)
                        self.write(RF_PHY.tx_test(mod, psdu, f1, p1, tx_attn_manual, tx_attn_rfic, tx_attn_digital,
                                                  txContinuousMode, numOfPacket, pkt_intval * 1000, txCWMode, ant))
                        time.sleep(0.15)
                        m_sa.setPeakSearch()
                        t = round(m_sa.getMarkerY(), 2)
                        sheet1.write(f_count + 1, p_count + 1, t)
                        if m_mainWindow.m_txFreqOffsetEnable.isChecked():
                            freq = m_sa.getMarkerX()
                            ppm = round(1e3 * (freq - f1 * 1e3) / f1, 2)
                            sheet2.write(f_count + 1, p_count + 1, ppm)
                        print(str(t) + 'dBm at ' + str(f1) + ' KHz, ' + str(p1 * 0.5) + ' setting')
                        self.write(RF_PHY.tx_stop())
                        p_count = p_count + 1
                    f_count = f_count + 1
                wb.close()
            else:  # normal tx test mode...
                self.write(
                    RF_PHY.tx_test(mod, psdu, f, p, tx_attn_manual, tx_attn_rfic, tx_attn_digital, txContinuousMode,
                                   numOfPacket, pkt_intval * 1000, txCWMode, ant))
        else:  # normal tx mode... this is not working....
            duration = float(m_mainWindow.m_txDuration.text())
            for i in range(numOfPacket):
                self.write(RF_PHY.tx(mod, psdu, f, p))
                time.sleep((duration + pkt_intval) * 0.001)

    def slot_stopTx(self):
        self.write(RF_PHY.tx_stop())


    def slot_startACLR(self, m_mainWindow, m_sa):
        (mod, psdu, f, p, pkt_intval, numOfPacket) = self.get_txParameters(m_mainWindow)
        if mod in [0, 2, 3]:
            m_sa.setACLR(300000)
            m_mainWindow.m_txFreqStep.clear()
            m_mainWindow.m_txFreqStep.insert("0.3")
        elif 0x20 < mod < 0x30:  # OFDM option 1
            m_sa.setACLR(1200000)
            m_mainWindow.m_txFreqStep.clear()
            m_mainWindow.m_txFreqStep.insert("1.2")
        else:
            m_sa.setACLR(400000)
            m_mainWindow.m_txFreqStep.clear()
            m_mainWindow.m_txFreqStep.insert("0.4")
        (tx_attn_manual, tx_attn_rfic, tx_attn_digital, txContinuousMode, txCWMode,
         ant) = self.get_txTestModeParameters(
            m_mainWindow)
        f_stop = int(float(m_mainWindow.m_txFreqStop.text()) * 1000)
        f_step = int(float(m_mainWindow.m_txFreqStep.text()) * 1000)
        if (f_stop - f) % f_step == 0:
            f_stop = f_stop + f_step
        f_num = math.ceil((f_stop - f) / f_step)
        t = [0 for i in range(28)]
        f_count = 0

        timestamp = datetime.datetime.now().strftime("%m_%d_%H_%M")
        wb = xlsxwriter.Workbook('tx_aclr_sweep_' + timestamp + '.xlsx')
        sheet1 = wb.add_worksheet('ACLR')
        sheet1.write(0, 1, 'Total Car Pwr')
        sheet1.write(0, 2, 'Lower adjacent(dBc)')
        sheet1.write(0, 3, 'Lower adjacent(dBm)')
        sheet1.write(0, 4, 'Upper adjacent(dBc)')
        sheet1.write(0, 5, 'Upper adjacent(dBm)')
        sheet1.write(0, 6, 'Lower alternate(dBc)')
        sheet1.write(0, 7, 'Lower alternate(dBm)')
        sheet1.write(0, 8, 'Upper alternate(dBc)')
        sheet1.write(0, 9, 'Upper alternate(dBm)')
        sheet1.write(0, 10, '2nd lower alternate(dBc)')
        sheet1.write(0, 11, '2nd lower alternate(dBm)')
        sheet1.write(0, 12, '2nd upper alternate(dBc)')
        sheet1.write(0, 13, '2nd upper(alternatedBm)')

        f_xls = f
        for i in range(f_num):
            sheet1.write(i + 1, 0, f_xls)
            f_xls = f_xls + f_step
        for f1 in range(f, f_stop, f_step):
            m_sa.setCenterFreq(f1 * 1e3)
            self.write(RF_PHY.tx_test(mod, psdu, f1, p, tx_attn_manual, tx_attn_rfic, tx_attn_digital, txContinuousMode,
                                      numOfPacket, pkt_intval * 1000, txCWMode, ant))
            print('Running at ' + str(f1) + ' KHz')
            t = m_sa.getACLR()
            self.write(RF_PHY.tx_stop())
            sheet1.write(f_count + 1, 1, round(t[1], 2))
            for i in range(12):
                sheet1.write(f_count + 1, i + 2, round(t[i + 4], 2))
            f_count = f_count + 1
        wb.close()

    "get and return tx parameters from the GUI"

    def get_txParameters(self, m_mainWindow):
        mod = m_mainWindow.m_modVal[m_mainWindow.m_txMod.currentIndex()]
        psdu = int(m_mainWindow.psdulen.text())
        f = int(float(m_mainWindow.m_txFreq.text()) * 1000)  # frequency in KHz so that it works with API
        p = m_mainWindow.m_txPower.currentIndex()
        pkt_intval = int(m_mainWindow.m_gap.text())
        numOfPacket = int(m_mainWindow.m_numOfPacket.text())
        return mod, psdu, f, p, pkt_intval, numOfPacket

    "get and return  tx test mode parameters from the GUI"

    def get_txTestModeParameters(self, m_mainWindow):
        tx_attn_manual = int(m_mainWindow.m_levelSet.isChecked())
        tx_attn_rfic = m_mainWindow.m_RFIC.currentIndex()
        tx_attn_digital = int(m_mainWindow.m_DMCC.text())
        txContinuousMode = int(m_mainWindow.m_txContinuous.isChecked())
        txCWMode = int(m_mainWindow.m_txCW.isChecked())
        ant = m_mainWindow.m_ant.currentIndex()
        return tx_attn_manual, tx_attn_rfic, tx_attn_digital, txContinuousMode, txCWMode, ant

    def slot_rx(self, m_mainWindow, sg):
        f = int(float(m_mainWindow.m_rxFreq.text()) * 1000)
        if m_mainWindow.m_rxLoopEnable.isChecked():  # rx loop test section, ACT modulation config
            f_stop = int(float(m_mainWindow.m_rxFreqStop.text()) * 1000)
            f_step = int(float(m_mainWindow.m_rxFreqStep.text()) * 1000)
            if (f_stop - f) % f_step == 0:
                f_stop = f_stop + f_step
            f_num = math.ceil((f_stop - f) / f_step)
            cableLoss = float(m_mainWindow.m_cableLoss.text())
            p_start = int(m_mainWindow.m_rxPowerStart.text())
            p_stop = int(m_mainWindow.m_rxPowerStop.text())
            p_step = int(m_mainWindow.m_rxPowerStep.text())
            if (p_stop - p_start) % p_step == 0:
                p_stop = p_stop + p_step
            p_num = math.ceil((p_stop - p_start) / p_step)
            f_count = 0
            timestamp = datetime.datetime.now().strftime("%m_%d_%H_%M")
            wb = xlsxwriter.Workbook('rssi_sweep_' + timestamp + '.xlsx')
            sheet1 = wb.add_worksheet('RSSI')
            f_xls = f
            p_xls = p_start
            for i in range(f_num):
                sheet1.write(i + 1, 0, f_xls)
                f_xls = f_xls + f_step
            for i in range(p_num):
                sheet1.write(0, i + 1, float(p_xls))
                p_xls = p_xls + p_step
            for f1 in range(f, f_stop, f_step):  # frequency loop...
                p_count = 0
                if m_mainWindow.m_rxTestMode.isChecked():  # rx test mode
                    self.write(RF_PHY.rx_config_test_mode(f1))
                else:
                    self.write(RF_PHY.rx_config(f1))
                sg.setFreq((f1 + 50) * 1000)
                for p1 in range(p_start, p_stop, p_step):  # power loop...
                    sg.rfOn(False)
                    sg.setPower(p1 + cableLoss)  # configure the power of signal generator
                    sg.rfOn(True)
                    time.sleep(0.2)  # turn on RF and wait
                    self.write(RF_PHY.rssi_req())  # request for RSSI read
                    time.sleep(0.25)
                    rssi_floor = m_mainWindow.noiseFloor
                    sheet1.write(f_count + 1, p_count + 1, rssi_floor)
                    print(str(rssi_floor) + 'dBm, ' + str(f1) + ' KHz, ' + str(p1) + ' dBm input')
                    p_count = p_count + 1
                f_count = f_count + 1
                sg.rfOn(False)
            wb.close()
            return
        if m_mainWindow.m_rxTestMode.isChecked():  # rx test mode
            self.write(RF_PHY.rx_config_test_mode(f))
        else:  # normal rx mode
            self.write(RF_PHY.rx_config(f))

    def slot_rssiReq(self):
        self.write(RF_PHY.rssi_req())

    def slot_sensitivity_test_mode(self, m_mainWindow, sg):
        self.thread.terminate()
        sg.config_for_packets()
        f, f_stop, f_step, f_num, p_start, p_stop, p_step, p_num, cableLoss, nop, data_rate = self.getRxParameters(
            m_mainWindow)
        for i in range(len(data_rate)):
            if data_rate[i][0] == 0x24 or data_rate[i][0] == 0x26:
                sg.setSamplingClock(15e6)
            else:
                sg.setSamplingClock(7.5e6)
            sg.setWaveform(data_rate[i][1])
            print('Testing ' + data_rate[i][1] + '...')
            target_pwr = data_rate[i][2]
            packet_gap = data_rate[i][3]
            f_count = 0
            timestamp = datetime.datetime.now().strftime("%m_%d_%H_%M")
            wb = xlsxwriter.Workbook(data_rate[i][1] + '_' + timestamp + 'RSSI.xlsx')
            sheet1 = wb.add_worksheet('Summary')
            sheet2 = wb.add_worksheet(str(data_rate[i][1]))
            sheet1.write(0, 1, data_rate[i][1])
            f_xls = f
            for j in range(f_num):
                sheet1.write(j + 1, 0, f_xls)
                sheet2.write(j + 1, 0, f_xls)
                f_xls = f_xls + f_step
            for k in range(7):
                sheet2.write(0, k + 1, target_pwr - 1 + k)

            for f1 in range(f, f_stop, f_step):  # frequency loop...
                if data_rate[i][0] == 8 or data_rate[i][0] == 0x82:  # FSK150k and LR12.5k use old configure...
                    self.write(RF_PHY.rx_config_test_mode(f1))
                else:
                    self.write(RF_PHY.rx_config_test_mode_gen(f1))
                sg.setFreq(f1 * 1000)
                p_count = 0
                per = 1
                for p1 in range(target_pwr - 1, target_pwr + 5, 1):  # power loop...
                    sg.setPower(p1 + cableLoss)
                    sg.send_packets(nop, packet_gap)
                    self.m_serialPort.reset_input_buffer()  # clear serial input buffer
                    self.write(RF_PHY.rx_test_mode_get_counters())
                    time.sleep(0.1)
                    t = RF_PHY.protocal_unpack(self.read())
                    if 0x20 < data_rate[i][0] < 0x50:
                        ppdu = RF_PHY.TwoBytesToUShort(t[90:92])
                    elif data_rate[i][0] == 0x82:
                        ppdu = RF_PHY.TwoBytesToUShort(t[118:120])
                    else:
                        ppdu = RF_PHY.TwoBytesToUShort(t[62:64])
                    print('Received ' + str(ppdu) + ' packets, ' + str(f1) + ' KHz, ' + str(p1) + ' dBm')
                    sheet2.write(f_count + 1, p_count + 1, ppdu)
                    p_count = p_count + 1
                    self.write(RF_PHY.rx_test_mode_clear_counters())
                    previous_per = per
                    per = (nop - ppdu) / nop
                    if per <= 0.1 and previous_per >= 0.1:
                        sheet1.write(f_count + 1, 1, p1)
                        break
                f_count = f_count + 1
            wb.close()
        sg.rfOn(False)
        self.thread.start()

    "Read single packet RSSI while sweeping frequency and power levels"

    def slot_rssi_sweep(self, m_mainWindow, sg):
        sg.config_for_packets()
        f, f_stop, f_step, f_num, p_start, p_stop, p_step, p_num, cableLoss, nop, data_rate = self.getRxParameters(
            m_mainWindow)
        nop = 1
        for i in range(len(data_rate)):
            if data_rate[i][0] == 0x24 or data_rate[i][0] == 0x26:
                sg.setSamplingClock(15e6)
            else:
                sg.setSamplingClock(7.5e6)
            sg.setWaveform(data_rate[i][1])
            print('Testing ' + data_rate[i][1] + '...')
            packet_gap = data_rate[i][3]
            f_count = 0
            timestamp = datetime.datetime.now().strftime("%m_%d_%H_%M")
            wb = xlsxwriter.Workbook(data_rate[i][1] + '_' + timestamp + 'RSSI.xlsx')
            sheet1 = wb.add_worksheet('Packet_RSSI')
            sheet1.write(0, 1, data_rate[i][1])
            f_xls = f
            for j in range(f_num):
                sheet1.write(j + 1, 0, f_xls)
                f_xls = f_xls + f_step
            p_xls = p_start
            for k in range(p_num):
                sheet1.write(0, k + 1, float(p_xls))
                p_xls = p_xls + p_step
            for f1 in range(f, f_stop, f_step):  # frequency loop...
                if data_rate[i][0] == 8 or data_rate[i][0] == 0x82:  # FSK150k and LR12.5k use old configure...
                    self.write(RF_PHY.rx_config(f1))
                else:
                    self.write(RF_PHY.rx_config_gen(f1))
                sg.setFreq(f1 * 1000)
                p_count = 0
                for p1 in range(p_start, p_stop, p_step):  # power loop...
                    sg.setPower(p1 + cableLoss)
                    sg.send_packets(nop, packet_gap)
                    time.sleep(0.2)
                    rssi = m_mainWindow.pkt_rssi
                    print('Received a packet at ' + str(f1) + ' KHz, ' + str(p1) + ' dBm, RSSI ' + str(rssi))
                    sheet1.write(f_count + 1, p_count + 1, rssi)
                    p_count = p_count + 1
                f_count = f_count + 1
            wb.close()
        sg.rfOn(False)

    def slot_sensitivity(self, m_mainWindow, sg):  # TODO OFDM is not working
        sg.config_for_packets()
        f, f_stop, f_step, f_num, p_start, p_stop, p_step, p_num, cableLoss, nop, data_rate = self.getRxParameters(
            m_mainWindow)
        pwr_num = 8
        for i in range(len(data_rate)):
            if data_rate[i][0] == 0x24 or data_rate[i][0] == 0x26:
                sg.setSamplingClock(15e6)
            else:
                sg.setSamplingClock(7.5e6)
            sg.setWaveform(data_rate[i][1])
            print('Testing ' + data_rate[i][1] + '...')
            target_pwr = data_rate[i][2]
            packet_gap = data_rate[i][3]
            f_count = 0
            timestamp = datetime.datetime.now().strftime("%m_%d_%H_%M")
            wb = xlsxwriter.Workbook(data_rate[i][1] + '_' + timestamp + '.xlsx')
            sheet1 = wb.add_worksheet('Summary')
            sheet2 = wb.add_worksheet(str(data_rate[i][1]))
            sheet1.write(0, 1, data_rate[i][1])
            f_xls = f
            for j in range(f_num):
                sheet1.write(j + 1, 0, f_xls)
                sheet2.write(j + 1, 0, f_xls)
                f_xls = f_xls + f_step
            for k in range(pwr_num):
                sheet2.write(0, k + 1, target_pwr - 1 + k)
            for f1 in range(f, f_stop, f_step):  # frequency loop...
                if data_rate[i][0] == 8 or data_rate[i][0] == 0x82:  # FSK150k and LR12.5k use old configure...
                    self.write(RF_PHY.rx_config(f1))
                else:
                    self.write(RF_PHY.rx_config_gen(f1))
                sg.setFreq(f1 * 1000)
                p_count = 0
                per = 1
                for p1 in range(target_pwr - 1, target_pwr + pwr_num - 2, 1):  # power loop...
                    m_mainWindow.fskCounter = 0
                    m_mainWindow.ofdmCounter = 0
                    m_mainWindow.oqpskCounter = 0
                    sg.setPower(p1 + cableLoss)
                    sg.send_packets(nop, packet_gap)
                    time.sleep(0.15)
                    if data_rate[i][0] < 0x10:
                        ppdu = m_mainWindow.fskCounter
                    elif data_rate[i][0] < 0x50:
                        ppdu = m_mainWindow.ofdmCounter
                    else:
                        ppdu = m_mainWindow.oqpskCounter
                    print('Received ' + str(ppdu) + ' packets, ' + str(f1) + ' KHz, ' + str(p1) + ' dBm')
                    sheet2.write(f_count + 1, p_count + 1, ppdu)
                    p_count = p_count + 1
                    previous_per = per
                    per = (nop - ppdu) / nop
                    if per <= 0.1 and previous_per >= 0.1:
                        sheet1.write(f_count + 1, 1, p1)
                        break
                f_count = f_count + 1
            wb.close()
        sg.rfOn(False)

    def getRxParameters(self, m_mainWindow):
        f = int(float(m_mainWindow.m_rxFreq.text()) * 1000)
        f_stop = int(float(m_mainWindow.m_rxFreqStop.text()) * 1000)
        f_step = int(float(m_mainWindow.m_rxFreqStep.text()) * 1000)
        if (f_stop - f) % f_step == 0:
            f_stop = f_stop + f_step
        f_num = math.ceil((f_stop - f) / f_step)
        p_start = int(m_mainWindow.m_rxPowerStart.text())
        p_stop = int(m_mainWindow.m_rxPowerStop.text())
        p_step = int(m_mainWindow.m_rxPowerStep.text())
        if (p_stop - p_start) % p_step == 0:
            p_stop = p_stop + p_step
        p_num = math.ceil((p_stop - p_start) / p_step)
        cableLoss = float(m_mainWindow.m_cableLoss.text())
        num_of_packets = int(m_mainWindow.m_packets.text())
        data_rate = []
        if m_mainWindow.m_FSK150k.isChecked():
            data_rate.append([8, 'RFPHY_MRFSK_150_250B', -109, 28.6])
        if m_mainWindow.m_OFDM200k.isChecked():
            data_rate.append([0x43, 'RFPHY_MROFDM_OPT3_MCS3', -110, 11.8])
        if m_mainWindow.m_OFDM600k.isChecked():
            data_rate.append([0x46, 'RFPHY_MROFDM_OPT3_MCS6', -101, 5])
        if m_mainWindow.m_LR125k.isChecked():
            data_rate.append([0x82, 'RFPHY_MROQPSK_12_5_20B', -122, 36.7])
        if m_mainWindow.m_SSNFSK100k.isChecked():
            data_rate.append([0x100, 'RFPHY_SSNFSK_100_250B', -104, 22.7])
        if m_mainWindow.m_SSNFSK150k.isChecked():
            data_rate.append([0x101, 'RFPHY_SSNFSK_150_250B', -102, 16.1])
        if m_mainWindow.m_SSNGFSK150k.isChecked():
            data_rate.append([0x102, 'RFPHY_SSNGFSK_150_250B', -101, 16.1])
        if m_mainWindow.m_SSNGFSK200k.isChecked():
            data_rate.append([0x102, 'RFPHY_SSNGFSK_200_250B', -101, 12.7])
        if m_mainWindow.m_SSNGFSK300k.isChecked():
            data_rate.append([0x102, 'RFPHY_SSNGFSK_300_250B', -99, 9])
        if m_mainWindow.m_OFDM1200k.isChecked():
            data_rate.append([0x24, 'RFPHY_MROFDM_OPT1_MCS4', -103, 5])
        if m_mainWindow.m_OFDM2400k.isChecked():
            data_rate.append([0x26, 'RFPHY_MROFDM_OPT1_MCS6', -98, 5])
        return f, f_stop, f_step, f_num, p_start, p_stop, p_step, p_num, cableLoss, num_of_packets, data_rate


class parse(QThread):
    def __init__(self, m_mainWindow, parent=None):
        QThread.__init__(self, parent)
        self.m = m_mainWindow

    def run(self):
        s = []
        while True:
            time.sleep(0.05)
            # t = b''
            # if self.m.m_serialPort.m_serialPort.is_open:
            # bytesToRead = self.m.m_serialPort.m_serialPort.inWaiting()
            t = self.m.m_serialPort.m_serialPort.read(2048)  # TODO bug here
            if t:
                for i in range(len(t)):
                    s.append(t[i])
            while 62 in s:
                ind = s.index(62)
                msg = RF_PHY.protocal_unpack(s[0:ind + 1])
                # print(msg)
                if msg[0:2] == RF_PHY.ITRON_DATA_INDICATION:  # only accept our test packet
                    if msg[2] < 0x10 and msg[14] == 250:
                        self.m.fskCounter += 1
                        self.m.m_fskCounter.clear()
                        self.m.m_fskCounter.insert(str(self.m.fskCounter))
                        self.m.pkt_rssi = RF_PHY.TwoBytesToShort(msg[40:42]) * 0.5
                        self.m.m_pkt_rssi.clear()
                        self.m.m_pkt_rssi.insert(str(self.m.pkt_rssi))
                    elif 0x20 < msg[2] < 0x50 and msg[14] == 250:
                        self.m.ofdmCounter += 1
                        self.m.m_ofdmCounter.clear()
                        self.m.m_ofdmCounter.insert(str(self.m.ofdmCounter))
                        self.m.pkt_rssi = RF_PHY.TwoBytesToShort(msg[40:42]) * 0.5
                        self.m.m_pkt_rssi.clear()
                        self.m.m_pkt_rssi.insert(str(self.m.pkt_rssi))
                    elif msg[2] > 0x60 and msg[14] == 20:
                        self.m.oqpskCounter += 1
                        self.m.m_oqpskCounter.clear()
                        self.m.m_oqpskCounter.insert(str(self.m.oqpskCounter))
                        self.m.pkt_rssi = RF_PHY.TwoBytesToShort(msg[40:42]) * 0.5
                        self.m.m_pkt_rssi.clear()
                        self.m.m_pkt_rssi.insert(str(self.m.pkt_rssi))
                elif msg[0:2] == RF_PHY.ITRON_STATUS_RESPONSE:  # RSSI noise floor
                    self.m.m_rssi.clear()
                    self.m.noiseFloor = RF_PHY.TwoBytesToShort(msg[12:14]) * 0.5
                    self.m.m_rssi.insert(str(self.m.noiseFloor))
                elif msg[0:2] == RF_PHY.ITRON_OTP_READ_RESP:  # OTP read
                    print(msg[11])
                s = s[ind + 1:]
