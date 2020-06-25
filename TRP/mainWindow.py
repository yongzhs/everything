from PyQt5.QtWidgets import (QAction, QCheckBox, QComboBox, QDialog, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLineEdit, QPushButton, QTextEdit, QToolBar, QWidget)
import spectrumAnalyzer
import rotator
import serialPort

import datetime
import math
import matplotlib.pyplot as plt
import numpy as np
import time
import xlsxwriter


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.sa = spectrumAnalyzer.spectrumAnalyzer()
        self.r = rotator.rotator()
        self.serialPort = serialPort.serialPort()

        self.containerWidget = QWidget(self)
        self.m_port = QComboBox(self.containerWidget)
        self.m_connectPort = QPushButton("Connect", self.containerWidget)
        self.m_disconnectPort = QPushButton("Disconnect", self.containerWidget)
        self.m_disconnectPort.setEnabled(False)
        self.m_freq = QLineEdit(self.containerWidget)
        self.m_pin = QLineEdit(self.containerWidget)
        self.m_distance = QLineEdit(self.containerWidget)
        self.m_gain = QLineEdit(self.containerWidget)
        self.m_cableLoss = QLineEdit(self.containerWidget)
        self.m_correctionFactor = QLineEdit(self.containerWidget)
        self.m_start = QPushButton("Start TRP", self.containerWidget)
        self.m_stop = QPushButton("Stop TRP", self.containerWidget)
        self.groupBox = QGroupBox("TRP", self)

        self.setWindowTitle("TRP")
        self.createBox()

        """ Toolbar section for equipments """
        m_toolbars = QToolBar()
        m_sa_panel = QAction("Spectrum analyzer", self)
        m_toolbars.addAction(m_sa_panel)
        m_sa_panel.triggered.connect(lambda: self.sa.show())
        m_rotator_panel = QAction("Rotator", self)
        m_toolbars.addAction(m_rotator_panel)
        m_rotator_panel.triggered.connect(lambda: self.r.show())
        m_toolbars.setMovable(False)

        layout = QGridLayout()
        layout.addWidget(m_toolbars)
        layout.addWidget(self.groupBox, 1, 0)
        self.setLayout(layout)


    """ delete objects on closing in destructor """
    def closeEvent(self, event):
        del self.sa, self.r

    '''  Create Tx management Box        '''
    def createBox(self):
        formLayout = QFormLayout(self.containerWidget)
        m_scanPort = QPushButton("Scan", self.containerWidget)
        m_portHBox = QHBoxLayout(self.containerWidget)
        m_portHBox.addWidget(m_scanPort)
        m_portHBox.addWidget(self.m_port)
        formLayout.addRow(m_portHBox)
        m_connectDisconnectHBox = QHBoxLayout(self.containerWidget)
        m_connectDisconnectHBox.addWidget(self.m_connectPort)
        m_connectDisconnectHBox.addWidget(self.m_disconnectPort)
        formLayout.addRow(m_connectDisconnectHBox)

        self.m_freq.insert("902")
        formLayout.addRow("Freq (MHz)", self.m_freq)
        self.m_pin.insert("10")
        formLayout.addRow("Pin (dBm)", self.m_pin)
        self.m_distance.insert("1.7")
        formLayout.addRow("Distance (m)", self.m_distance)
        self.m_gain.insert("7")
        formLayout.addRow("Antenna gain (dB)", self.m_gain)
        self.m_cableLoss.insert("1.2")
        formLayout.addRow("Cable loss (dB)", self.m_cableLoss)
        self.m_correctionFactor.setEnabled(False)
        formLayout.addRow("Correction factor (dB)", self.m_correctionFactor)

        m_startStopTxHBox = QHBoxLayout(self.containerWidget)
        m_startStopTxHBox.addWidget(self.m_start)
        m_startStopTxHBox.addWidget(self.m_stop)
        formLayout.addRow(m_startStopTxHBox)

        self.groupBox.setLayout(formLayout)

        self.serialPort.slot_listPorts(self)
        self.slot_calcCorrectionFactor()

        m_scanPort.clicked.connect(lambda: self.serialPort.slot_listPorts(self))
        self.m_connectPort.clicked.connect(lambda: self.serialPort.slot_openUart(self))
        self.m_disconnectPort.clicked.connect(lambda: self.serialPort.slot_closeUart(self))
        self.m_cableLoss.editingFinished.connect(self.slot_calcCorrectionFactor)
        self.m_start.clicked.connect(self.slot_trp)

    def slot_trp(self):
        n_theta = 13            # [0:15:180]
        step_theta = 180/(n_theta - 1)
        n_phi = 24              # [0:15:345]
        step_phi = 360/n_phi
        cf = float(self.m_correctionFactor.text())
        peak_eirp = -50         # in dBm
        trp = 0                 # in mW
        pin = float(self.m_pin.text())
        gain_array = np.zeros([n_theta, n_phi], dtype=float)

        timestamp = datetime.datetime.now().strftime("%m_%d_%H_%M")
        wb = xlsxwriter.Workbook('trp_' + timestamp + '.xlsx')
        sheet1 = wb.add_worksheet('Summary')
        sheet2 = wb.add_worksheet('Raw_data')
        sheet3 = wb.add_worksheet('After_correction')
        sheet4 = wb.add_worksheet('EIRP')
        sheet5 = wb.add_worksheet("Gain")
        sheet6 = wb.add_worksheet("Plots")

        sheet1.write(0, 0, "Frequency (MHz)")
        sheet1.write(0, 1, float(self.m_freq.text()))
        sheet1.write(1, 0, "TRP (dBm)")
        sheet1.write(2, 0, "Peak EIRP (dBm)")
        sheet1.write(3, 0, "Directivity (dBi)")
        sheet1.write(4, 0, "Input power (dBm)")
        sheet1.write(4, 1, pin)
        sheet1.write(5, 0, "Efficiency (dB)")
        sheet1.write(6, 0, "Efficiency (%)")
        sheet1.write(7, 0, "Gain (dBi)")
        sheet1.write(9, 0, "Distance (m)")
        sheet1.write(9, 1, float(self.m_distance.text()))
        sheet1.write(10, 0, "Antenna gain (dB)")
        sheet1.write(10, 1, float(self.m_gain.text()))
        sheet1.write(11, 0, "Cable loss (dB)")
        sheet1.write(11, 1, float(self.m_cableLoss.text()))
        sheet1.write(12, 0, "Path loss (dB)")
        sheet1.write(12, 1, cf)
        sheet2.write(0, 0, "Raw Horizontal Results")
        sheet2.write(1, 0, "THETA\PHI")
        sheet2.write(n_theta + 2, 0, "Raw Vertical Results")
        sheet2.write(n_theta + 3, 0, "THETA\PHI")
        for i in range(n_theta):
            sheet2.write(i + 2, 0, i * step_theta)
            sheet2.write(i + n_theta + 4, 0, i * step_theta)
        for j in range(n_phi):
            sheet2.write(1, j + 1, j * step_phi)
            sheet2.write(n_theta + 3, j + 1, j * step_phi)
        sheet3.write(0, 0, "Horizontal Results after correction")
        sheet3.write(1, 0, "THETA\PHI")
        sheet3.write(n_theta + 2, 0, "Raw Vertical Results after correction")
        sheet3.write(n_theta + 3, 0, "THETA\PHI")
        for i in range(n_theta):
            sheet3.write(i + 2, 0, i * step_theta)
            sheet3.write(i + n_theta + 4, 0, i * step_theta)
        for j in range(n_phi):
            sheet3.write(1, j + 1, j * step_phi)
            sheet3.write(n_theta + 3, j + 1, j * step_phi)
        sheet4.write(0, 0, "Total EIRP (dBm)")
        sheet4.write(1, 0, "THETA\PHI")
        sheet4.write(n_theta + 2, 0, "Total EIRP (mW)")
        sheet4.write(n_theta + 3, 0, "THETA\PHI")
        for i in range(n_theta):
            sheet4.write(i + 2, 0, i * step_theta)
            sheet4.write(i + n_theta + 4, 0, i * step_theta)
        for j in range(n_phi):
            sheet4.write(1, j + 1, j * step_phi)
            sheet4.write(n_theta + 3, j + 1, j * step_phi)
        sheet5.write(0, 0, "Gain (dB)")
        sheet5.write(0, 1, "EIRP - Pin")
        sheet5.write(1, 0, "THETA\PHI")
        for i in range(n_theta):
            sheet5.write(i + 2, 0, i * step_theta)
        for j in range(n_phi):
            sheet5.write(1, j + 1, j * step_phi)

        self.r.goto_phi(0)
        self.r.goto_theta(0)

        for i in range(n_theta):
            self.r.goto_theta(i * step_theta)
            print("Moving to theta: " + str(i * step_theta))
            while self.r.theta_busy:
                time.sleep(0.1)
            for j in range(n_phi):
                self.serialPort.vertical(0)

                self.r.goto_phi(j * step_phi)
                print("Moving to phi: " + str(j * step_phi))
                while self.r.phi_busy:
                    time.sleep(0.1)
                self.sa.setPeakSearch()
                h = self.sa.getMarkerY()
                sheet2.write(i + 2, j + 1, h)
                sheet3.write(i + 2, j + 1, h + cf)

                self.serialPort.vertical(1)
                time.sleep(0.5)
                self.sa.setPeakSearch()
                v = self.sa.getMarkerY()
                sheet2.write(i + n_theta + 4, j + 1, v)
                sheet3.write(i + n_theta + 4, j + 1, v + cf)

                eirp = 10**((v + cf)/10) + 10**((h + cf)/10)
                sheet4.write(i + n_theta + 4, j + 1, eirp)          # write eirp in mW
                eirp_dbm = 10 * math.log10(eirp)
                sheet4.write(i + 2, j + 1, eirp_dbm)                # write eirp in dBm
                g_temp = eirp_dbm - pin
                gain_array[i, j] = g_temp
                sheet5.write(i + 2, j + 1, g_temp)                  # write gain in dB
                if eirp > peak_eirp:
                    peak_eirp = eirp
                trp += eirp * math.sin(i * step_theta * math.pi /180) * step_theta * step_phi
        trp = 10 * math.log10(0.00002424 * trp)
        sheet1.write(1, 1, trp)
        sheet1.write(2, 1, peak_eirp)
        sheet1.write(3, 1, peak_eirp - trp)             # directivity
        sheet1.write(5, 1, trp - pin)                   # efficiency in dB
        sheet1.write(6, 1, 100*10**((trp - pin)/10))    # efficiency in percent
        sheet1.write(7, 1, peak_eirp - pin)             # gain
        # add plots, 3d plot, 2d plots, e and h planes

        wb.close()

        self.r.goto_phi(0)
        self.r.goto_theta(0)


    def slot_calcCorrectionFactor(self):
        fspl = 20 * math.log10(float(self.m_distance.text())) + 20 * math.log10(float(self.m_freq.text())) - 27.55
        cf = round(fspl + float(self.m_cableLoss.text()) - float(self.m_gain.text()), 2)
        self.m_correctionFactor.clear()
        self.m_correctionFactor.insert(str(cf))
