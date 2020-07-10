import visa
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QDialog, QFormLayout, QGroupBox, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget)


class spectrumAnalyzer(QDialog):
    def __init__(self):
        super().__init__()
        self.rm = visa.ResourceManager()
        self.rm.list_resources()

        self.setWindowTitle("Spectrum Analyzer")
        containerWidget = QWidget(self)
        formLayout = QFormLayout(containerWidget)

        self.address = QLineEdit(containerWidget)
        self.address.insert("USB0::0x2A8D::0x1A0B::MY55450128::0::INSTR") # 'TCPIP0::172.17.212.103::inst0::INSTR'
        formLayout.addRow("Address", self.address)

        self.m_connect = QPushButton("Connect", containerWidget)
        formLayout.addRow(self.m_connect)

        self.m_saStartFreq = QLineEdit(containerWidget)
        self.m_saStartFreq.insert("900")
        formLayout.addRow("Start Frequency (MHz)", self.m_saStartFreq)
        self.m_saStopFreq = QLineEdit(containerWidget)
        self.m_saStopFreq.insert("930")
        formLayout.addRow("Stop Frequency (MHz)", self.m_saStopFreq)
        self.m_saCenterFreq = QLineEdit(containerWidget)
        self.m_saCenterFreq.insert("915")
        formLayout.addRow("Center Frequency (MHz)", self.m_saCenterFreq)
        self.m_saSpan = QLineEdit(containerWidget)
        self.m_saSpan.insert("1")
        formLayout.addRow("Span (MHz)", self.m_saSpan)

        self.m_saExternalGain = QLineEdit(containerWidget)
        self.m_saExternalGain.insert("-10.8")
        formLayout.addRow("External Gain (dB)", self.m_saExternalGain)
        self.m_saRefLevel = QLineEdit(containerWidget)
        self.m_saRefLevel.insert("30")
        formLayout.addRow("Ref Level (dBm)", self.m_saRefLevel)
        self.m_saScale = QLineEdit(containerWidget)
        self.m_saScale.insert("10")
        formLayout.addRow("Scale (dB)", self.m_saScale)
        self.m_saAttenuation = QComboBox(containerWidget)
        for i in range(5):
            self.m_saAttenuation.insertItem(i, str(i * 10))
        self.m_saAttenuation.setCurrentIndex(3)
        formLayout.addRow("Attenuation (dB)", self.m_saAttenuation)

        self.m_saRBW = QLineEdit(containerWidget)
        self.m_saRBW.insert("100")
        formLayout.addRow("RBW (KHz)", self.m_saRBW)
        self.m_saVBW = QLineEdit(containerWidget)
        self.m_saVBW.insert("300")
        formLayout.addRow("VBW (KHz)", self.m_saVBW)

        self.m_saTrace = QComboBox(containerWidget)
        self.m_saTrace.insertItem(0, "ClearWrite")
        self.m_saTrace.insertItem(1, "Average")
        self.m_saTrace.insertItem(2, "MaxHold")
        formLayout.addRow("Trace", self.m_saTrace)

        self.m_saDetector = QComboBox(containerWidget)
        self.m_saDetector.insertItem(0, "Average")
        self.m_saDetector.insertItem(1, "Peak")
        self.m_saDetector.insertItem(2, "Normal")
        self.m_saDetector.insertItem(3, "Sample")
        self.m_saDetector.insertItem(4, "QPeak")
        self.m_saDetector.insertItem(5, "EMI Average")
        formLayout.addRow("Detector", self.m_saDetector)

        self.m_profileACLR = QLineEdit(containerWidget)
        self.m_profileACLR.insert("400")
        formLayout.addRow("ACLR (KHz)", self.m_profileACLR)

        self.m_saStartFreq.setEnabled(False)
        self.m_saStopFreq.setEnabled(False)
        self.m_saCenterFreq.setEnabled(False)
        self.m_saSpan.setEnabled(False)
        self.m_saRefLevel.setEnabled(False)
        self.m_saScale.setEnabled(False)
        self.m_saExternalGain.setEnabled(False)
        self.m_saAttenuation.setEnabled(False)
        self.m_saRBW.setEnabled(False)
        self.m_saVBW.setEnabled(False)
        self.m_saTrace.setEnabled(False)
        self.m_saDetector.setEnabled(False)
        self.m_profileACLR.setEnabled(False)

        self.groupBox = QGroupBox("Spectrum Analyzer", self)
        self.groupBox.setLayout(formLayout)
        layout = QVBoxLayout()
        layout.addWidget(self.groupBox)
        self.setLayout(layout)

        self.m_connect.clicked.connect(lambda: self.connect())
        self.m_saStartFreq.editingFinished.connect(lambda: self.setStartFreq(float(self.m_saStartFreq.text()) * 1e6))
        self.m_saStopFreq.editingFinished.connect(lambda: self.setStopFreq(float(self.m_saStopFreq.text()) * 1e6))
        self.m_saCenterFreq.editingFinished.connect(lambda: self.setCenterFreq(float(self.m_saCenterFreq.text()) * 1e6))
        self.m_saSpan.editingFinished.connect(lambda: self.setSpan(float(self.m_saSpan.text()) * 1e6))
        self.m_saExternalGain.editingFinished.connect(lambda: self.setExternalGain(float(self.m_saExternalGain.text())))
        self.m_saAttenuation.currentIndexChanged.connect(lambda: self.setAttenuation(int(self.m_saAttenuation.currentIndex()) * 10))
        self.m_saRefLevel.editingFinished.connect(lambda: self.setRefLevel(float(self.m_saRefLevel.text())))
        self.m_saScale.editingFinished.connect(lambda: self.setScale(float(self.m_saScale.text())))
        self.m_saRBW.editingFinished.connect(lambda: self.setRBW(int(self.m_saRBW.text()) * 1e3))
        self.m_saVBW.editingFinished.connect(lambda: self.setVBW(int(self.m_saVBW.text()) * 1e3))
        self.m_saTrace.currentIndexChanged.connect(lambda: self.setTrace(self.m_saTrace.currentIndex()))
        self.m_saDetector.currentIndexChanged.connect(lambda: self.setDetector(self.m_saDetector.currentIndex()))
        self.m_profileACLR.editingFinished.connect(lambda: self.setACLR(float(float(self.m_profileACLR.text()) * 1e3)))


    def __del__(self):  # destructor closes the port on closing if port is open
        self.rm.close()


    def connect(self):
        address = self.address.text()
        try:
            self.sa = self.rm.open_resource(address)
            print("Connected to " + self.sa.query('*IDN?'))
        except:
            print("Connection error!")
            return -1
        self.m_saStartFreq.setEnabled(True)
        self.m_saStopFreq.setEnabled(True)
        self.m_saCenterFreq.setEnabled(True)
        self.m_saSpan.setEnabled(True)
        self.m_saRefLevel.setEnabled(True)
        self.m_saScale.setEnabled(True)
        self.m_saExternalGain.setEnabled(True)
        self.m_saAttenuation.setEnabled(True)
        self.m_saRBW.setEnabled(True)
        self.m_saVBW.setEnabled(True)
        self.m_saTrace.setEnabled(True)
        self.m_saDetector.setEnabled(True)
        self.m_profileACLR.setEnabled(True)

    def setStartFreq(self, f):
        self.sa.write('FREQ:STAR %s' % f)  # page 658 of programming guide

    def setStopFreq(self, f):
        self.sa.write('FREQ:STOP ' + str(f))

    def setCenterFreq(self, f):  # page 1103 of programming guide
        self.sa.write('FREQ:CENT ' + str(f))

    def setSpan(self, f):  # page 1250 of programming guide
        self.sa.write('FREQ:SPAN ' + str(f))

    def setRefLevel(self, y):  # page 2893
        self.sa.write('DISP:WIND:TRAC:Y:RLEV ' + str(y) + ' dBm')

    def setScale(self, scale):
        self.sa.write('DISP:WIND:TRAC:Y:PDIV ' + str(scale))

    def setExternalGain(self, g):
        self.sa.write('CORR:SA:GAIN ' + str(g))

    def setAttenuation(self, a):  # page 2895
        self.sa.write('POWer:RF:ATTenuation ' + str(a))

    def setRBW(self, rbw):
        self.sa.write('BAND ' + str(rbw))

    def setVBW(self, vbw):  # page 636
        self.sa.write('BAND:VID ' + str(vbw))

    def setTrace(self, trace):
        if trace == 0:
            command = 'TRACe1:TYPE WRITe'
        elif trace == 1:
            command = 'TRACe1:TYPE AVERage'
        else:
            command = 'TRACe1:TYPE MAXHold'
        self.sa.write(command)

    def setDetector(self, det):  # page 994
        if det == 0:
            command = 'DETector:TRACe1 AVERage'
        elif det == 1:
            command = 'DETector:TRACe1 POSitive'
        elif det == 2:
            command = 'DETector:TRACe1 NORMal'
        elif det == 3:
            command = 'DETector:TRACe1 SAMPle'
        elif det == 4:
            command = 'DETector:TRACe1 QPEak'
        else:
            command = 'DETector:TRACe1 EAVerage'
        self.sa.write(command)

    def setPeakSearch(self):
        self.sa.write('CALC:MARK1:MAX')

    def getMarkerX(self):
        return float(self.sa.query('CALC:MARK1:X?'))

    def getMarkerY(self):
        return float(self.sa.query('CALC:MARK1:Y?'))

    def setACLR(self, bw):  # user shall configure the other parameters not listed here
        self.sa.write(':INITiate:CONTinuous 0')
        self.sa.write(':CONFigure:ACPower')  # go to acp mode
        self.sa.write('ACPower:AVERage:COUNt 10')  # set Avg count to 10
        self.sa.write('ACPower:CARRier:COUNt 1')  # Specifies the number of carriers to be measured to 1
        self.sa.write('FREQuency:CENTer:STEP:INCRement %G' % bw)  # frequency step
        self.sa.write(':DISPlay:ACPower:VIEW:WINDow:TRACe:Y:SCALe:RLEVel 30')
        self.sa.write(':SENSe:ACPower:OFFSet:OUTer:LIST:STATe 1, 1, 1, 0, 0, 0')
        self.sa.write('ACPower:BANDwidth:SHAPe GAUSsian')
        self.sa.write('ACPower:OFFSet:LIST:BWIDth:SHAPe GAUSsian, GAUSsian, GAUSsian, GAUSsian, GAUSsian, GAUSsian')
        self.sa.write('ACPower:OFFSet:OUTer:LIST:FREQuency %s,%s,%s,%s,%s,%s' % (bw, 2 * bw, 3 * bw, 0, 0, 0))
        self.sa.write('ACPower:OFFSet:OUTer:LIST:BANDwidth:INTegration %s,%s,%s,%s,%s,%s' % (bw, bw, bw, bw, bw, bw))
        self.sa.write(
            'ACPower:OFFSet:OUTer:LIST:SIDE %s,%s,%s,%s,%s,%s' % ('BOTH', 'BOTH', 'BOTH', 'BOTH', 'BOTH', 'BOTH'))
        self.sa.write('ACPower:CARRier:LIST:WIDTh %s' % bw)
        self.sa.write('ACPower:CARRier:LIST:BANDwidth:INTegration %s' % bw)
        self.sa.write('ACPower:FREQuency:SPAN %s' % (8 * bw))
        self.sa.write('ACP:BAND:AUTO ON')
        self.sa.write(':TRACe:ACPower:TYPE AVERage')
        self.sa.write(':FORMat:TRACe:DATA %s,%d' % ('REAL', 32))
        self.sa.write(':FORMat:BORDer SWAPped')

    def getACLR(self):
        self.sa.write(':INITiate:ACP')
        t = self.sa.query_binary_values(':FETCh:ACP?', 'f', False)  # return a list of float results here
        return t
