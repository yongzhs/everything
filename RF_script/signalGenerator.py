import visa 
import time
from PyQt5.QtWidgets import (QCheckBox, QDialog, QFormLayout, QGroupBox, QHBoxLayout, QLineEdit, QPushButton, QVBoxLayout, QWidget)


class signalGenerator(QDialog):  # the class works GUI application
    def __init__(self):
        super().__init__()
        self.rm = visa.ResourceManager()
        self.rm.list_resources()

        self.setWindowTitle("Signal Generator")
        containerWidget = QWidget(self)
        formLayout = QFormLayout(containerWidget)

        self.address = QLineEdit(containerWidget)
        self.address.insert("TCPIP0::172.17.212.14::inst0::INSTR")
        formLayout.addRow("Address ", self.address)

        self.m_connect = QPushButton("Connect", containerWidget)
        formLayout.addRow(self.m_connect)

        self.freq = QLineEdit(containerWidget)
        self.freq.insert("902.4")
        formLayout.addRow("Frequency (MHz)", self.freq)

        self.power = QLineEdit(containerWidget)
        self.power.insert("-80")
        formLayout.addRow("Power (dBm)", self.power)

        self.waveform = QLineEdit(containerWidget)
        self.waveform.insert("RFPHY_MRFSK_150_250B")
        formLayout.addRow("Packet", self.waveform)

        self.number_of_Packets = QLineEdit(containerWidget)
        self.number_of_Packets.insert("10")
        formLayout.addRow("Num", self.number_of_Packets)

        self.rfOnButton = QPushButton("RF ON", containerWidget)
        self.rfOffButton = QPushButton("RF OFF", containerWidget)
        sgHBox = QHBoxLayout(containerWidget)
        sgHBox.addWidget(self.rfOnButton)
        sgHBox.addWidget(self.rfOffButton)
        formLayout.addRow(sgHBox)

        self.modulationOnButton = QPushButton("Mod ON", containerWidget)
        self.modulationOffButton = QPushButton("Mod OFF", containerWidget)
        sgHBox1 = QHBoxLayout(containerWidget)
        sgHBox1.addWidget(self.modulationOnButton)
        sgHBox1.addWidget(self.modulationOffButton)
        formLayout.addRow(sgHBox1)

        self.arbOnButton = QPushButton("ARB ON", containerWidget)
        self.arbOffButton = QPushButton("ARB OFF", containerWidget)
        sgHBox2 = QHBoxLayout(containerWidget)
        sgHBox2.addWidget(self.arbOnButton)
        sgHBox2.addWidget(self.arbOffButton)
        formLayout.addRow(sgHBox2)

        self.sendPacketsButton = QPushButton("Send Packets", containerWidget)
        formLayout.addRow(self.sendPacketsButton)

        self.freq.setEnabled(False)
        self.power.setEnabled(False)
        self.waveform.setEnabled(False)
        self.rfOnButton.setEnabled(False)
        self.rfOffButton.setEnabled(False)
        self.modulationOnButton.setEnabled(False)
        self.modulationOffButton.setEnabled(False)
        self.arbOnButton.setEnabled(False)
        self.arbOffButton.setEnabled(False)
        self.sendPacketsButton.setEnabled(False)

        self.groupBox = QGroupBox("Signal Generator", self)
        self.groupBox.setLayout(formLayout)
        vLayout = QVBoxLayout()
        vLayout.addWidget(self.groupBox)
        self.setLayout(vLayout)

        self.m_connect.clicked.connect(lambda: self.connect())
        self.freq.editingFinished.connect(lambda: self.setFreq(float(self.freq.text()) * 1e6))
        self.power.editingFinished.connect(lambda: self.setPower(float(self.power.text())))
        self.waveform.editingFinished.connect(lambda: self.setWaveform(self.waveform.text()))
        self.rfOnButton.clicked.connect(lambda: self.rfOn(True))
        self.rfOffButton.clicked.connect(lambda: self.rfOn(False))
        self.modulationOnButton.clicked.connect(lambda: self.modulationOn(True))
        self.modulationOffButton.clicked.connect(lambda: self.modulationOn(False))
        self.arbOnButton.clicked.connect(lambda: self.ARBOn(True))
        self.arbOffButton.clicked.connect(lambda: self.ARBOn(False))
        self.sendPacketsButton.clicked.connect(lambda: self.send_packets_pb(int(self.number_of_Packets.text())))


    def __del__(self):
        self.rm.close()


    def connect(self):
        address = self.address.text()
        try:
            self.sg = self.rm.open_resource(address)
            print("Connected to " + self.sg.query('*IDN?'))
        except:
            print("Connection error!")
            return -1
        self.freq.setEnabled(True)
        self.power.setEnabled(True)
        self.waveform.setEnabled(True)
        self.rfOnButton.setEnabled(True)
        self.rfOffButton.setEnabled(True)
        self.modulationOnButton.setEnabled(True)
        self.modulationOffButton.setEnabled(True)
        self.arbOnButton.setEnabled(True)
        self.arbOffButton.setEnabled(True)
        self.sendPacketsButton.setEnabled(True)

    def setFreq(self, f):
        self.sg.write('FREQ ' + str(f))

    def setPower(self, p):
        self.sg.write('POW ' + str(p))

    def setSamplingClock(self, c):
        self.sg.write('SOURce:RADio:ARB:SCLock:RATE ' + str(c))

    def setWaveform(self, w):
        self.sg.write('SOURce:RADio:ARB:WAVeform "WFM1:' + str(w) + '"')

    def rfOn(self, on):
        if on == 1:
            self.sg.write('OUTPut:STATe on')
        else:
            self.sg.write('OUTPut:STATe off')

    def ARBOn(self, on):
        if on == 1:
            self.sg.write('RADio:ARB:STATe on')
        else:
            self.sg.write('RADio:ARB:STATe off')

    def modulationOn(self, on):
        if on == 1:
            self.sg.write(':OUTPut:MODulation on')
        else:
            self.sg.write(':OUTPut:MODulation off')

    def setTriggerType(self, t):  # set trigger type, continuous or single, gate type not included there
        if t == 0:  # continuous trigger
            self.sg.write('RADio:ARB:TRIGger:TYPE CONT')
        else:  # single trigger
            self.sg.write('RADio:ARB:TRIGger:TYPE SING')

    def setTriggerSource(self, s):
        if s == 0:
            self.sg.write(':SOURce:RADio:ARB:TRIGger:SOURce BUS')
        elif s == 1:
            self.sg.write(':SOURce:RADio:ARB:TRIGger:SOURce IMM')
        else:
            self.sg.write(':SOURce:RADio:ARB:TRIGger:SOURce External')

    def retriggerOn(self, on):
        if on == 1:
            self.sg.write(':SOURce:RADio:ARB:RETRigger ON')
        else:
            self.sg.write(':SOURce:RADio:ARB:RETRigger OFF')

    def ALCOn(self, on):
        if on == 1:
            self.sg.write('POWer:ALC ON')
        else:
            self.sg.write('POWer:ALC OFF')

    def config_for_packets(self):
        self.setTriggerType(1)
        self.setTriggerSource(0)
        self.retriggerOn(0)
        self.ALCOn(0)
        self.modulationOn(1)
        self.ARBOn(1)
        self.rfOn(1)

    def send_packets(self, nop, gap):
        self.sg.write(':SOURce:RADio:ARB:TRIGger:TYPE:SING:REP ' + str(nop))   # works only with N5182B new version...
        time.sleep(0.1)
        self.sg.write('*TRG')
        time.sleep(nop * gap * 1e-3)

    def send_packets_pb(self, nop):
        self.config_for_packets()
        self.sg.write(':SOURce:RADio:ARB:TRIGger:TYPE:SING:REP ' + str(nop))
        time.sleep(0.1)
        self.sg.write('*TRG')
