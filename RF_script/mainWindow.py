from PyQt5.QtWidgets import (QAction, QCheckBox, QComboBox, QDialog, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout,
                             QLineEdit, QPushButton, QTextEdit, QToolBar, QWidget)

import serialPort
import signalGenerator
import spectrumAnalyzer


class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.m_modVal = [0, 1, 2, 3, 4, 8, 0x24, 0x26, 0x43, 0X46, 0x82]
        self.fskCounter = 0
        self.ofdmCounter = 0
        self.oqpskCounter = 0
        self.pkt_rssi = 0
        self.noiseFloor = 0
        self.m_serialPort = serialPort.serialPort()
        self.m_spectrumAnalyzer = spectrumAnalyzer.spectrumAnalyzer()
        self.m_signalGenerator = signalGenerator.signalGenerator()

        self.m_txContainerWidget = QWidget(self)  # container for widgets in tx box
        self.m_port = QComboBox(self.m_txContainerWidget)
        self.m_connectPort = QPushButton("Connect", self.m_txContainerWidget)
        self.m_disconnectPort = QPushButton("Disconnect", self.m_txContainerWidget)
        self.m_disconnectPort.setEnabled(False)
        
        self.m_txMod = QComboBox(self.m_txContainerWidget)  # tx modulation selection
        self.psdulen = QLineEdit(self.m_txContainerWidget)  # psdu length
        self.m_txFreq = QLineEdit(self.m_txContainerWidget)  # tx frequency
        self.m_txPower = QComboBox(self.m_txContainerWidget)  # tx power selection
        self.m_numOfPacket = QLineEdit(self.m_txContainerWidget)  # tx number of packets
        self.m_gap = QLineEdit(self.m_txContainerWidget)  # tx interpacket gap
        self.m_txLoopEnable = QCheckBox("Loop test", self.m_txContainerWidget)  # tx loop test section
        self.m_txFreqOffsetEnable = QCheckBox("Freq offset", self.m_txContainerWidget)
        self.m_txFreqStop = QLineEdit(self.m_txContainerWidget)
        self.m_txFreqStep = QLineEdit(self.m_txContainerWidget)
        self.m_txPowerStop = QComboBox(self.m_txContainerWidget)
        self.m_txPowerStep = QComboBox(self.m_txContainerWidget)
        self.m_testMode = QCheckBox("Test mode", self.m_txContainerWidget)  # tx test mode
        self.m_levelSet = QCheckBox("Level set", self.m_txContainerWidget)
        self.m_RFIC = QComboBox(self.m_txContainerWidget)
        self.m_DMCC = QLineEdit(self.m_txContainerWidget)
        self.m_txContinuous = QCheckBox("Continuous", self.m_txContainerWidget)
        self.m_txCW = QCheckBox("CW", self.m_txContainerWidget)
        self.m_ant = QComboBox(self.m_txContainerWidget)
        self.m_txStart = QPushButton("Start TX", self.m_txContainerWidget)
        self.m_txStop = QPushButton("Stop TX", self.m_txContainerWidget)
        self.m_txACLR = QPushButton("ACLR test", self.m_txContainerWidget)
        self.txGroupBox = QGroupBox("Tx", self)

        self.m_rxContainerWidget = QWidget(self)
        self.rxGroupBox = QGroupBox("Rx", self)
        self.m_rxFreq = QLineEdit(self.m_rxContainerWidget)
        self.m_rxLoopEnable = QCheckBox("Loop test", self.m_rxContainerWidget)
        self.m_rxTestMode = QCheckBox("Test mode", self.m_rxContainerWidget)
        self.m_rxFreqStop = QLineEdit(self.m_rxContainerWidget)
        self.m_rxFreqStep = QLineEdit(self.m_rxContainerWidget)
        self.m_rxPowerStart = QLineEdit(self.m_rxContainerWidget)
        self.m_rxPowerStop = QLineEdit(self.m_rxContainerWidget)
        self.m_rxPowerStep = QLineEdit(self.m_rxContainerWidget)
        self.m_cableLoss = QLineEdit(self.m_rxContainerWidget)
        self.m_rssiRequest = QPushButton("Noise floor", self.m_rxContainerWidget)  # RSSI request, disabled by default
        self.m_rssi = QLineEdit(self.m_rxContainerWidget)
        self.m_rxConfig = QPushButton("Start Rx", self.m_rxContainerWidget)  # rx config and RSSI loop test
        self.m_fskCounter = QLineEdit(self.m_rxContainerWidget)
        self.m_ofdmCounter = QLineEdit(self.m_rxContainerWidget)
        self.m_oqpskCounter = QLineEdit(self.m_rxContainerWidget)
        self.m_pkt_rssi = QLineEdit(self.m_rxContainerWidget)
        self.m_FSK150k = QCheckBox("FSK150k", self.m_rxContainerWidget)
        self.m_OFDM200k = QCheckBox("OFDM200k", self.m_rxContainerWidget)
        self.m_OFDM600k = QCheckBox("OFDM600k", self.m_rxContainerWidget)
        self.m_LR125k = QCheckBox("LR12.5k", self.m_rxContainerWidget)
        self.m_SSNFSK100k = QCheckBox("SSNFSK100k", self.m_rxContainerWidget)
        self.m_SSNFSK150k = QCheckBox("SSNFSK150k", self.m_rxContainerWidget)
        self.m_SSNGFSK150k = QCheckBox("SSNGFSK150k", self.m_rxContainerWidget)
        self.m_SSNGFSK200k = QCheckBox("SSNGFSK200k", self.m_rxContainerWidget)
        self.m_SSNGFSK300k = QCheckBox("SSNGFSK300k", self.m_rxContainerWidget)
        self.m_OFDM1200k = QCheckBox("OFDM1200k", self.m_rxContainerWidget)
        self.m_OFDM2400k = QCheckBox("OFDM2400k", self.m_rxContainerWidget)
        self.m_packets = QLineEdit(self.m_rxContainerWidget)
        self.m_sensitivity = QPushButton("Sensitivity", self.m_rxContainerWidget)
        self.m_rssiSweep = QPushButton("RSSI sweep", self.m_rxContainerWidget)

        self.setWindowTitle("RF_PHY")
        self.createTxBox()
        self.createRxBox()

        """ Toolbar section for equipments """
        m_toolbars = QToolBar()
        m_sa_panel = QAction("Spectrum analyzer", self)
        m_toolbars.addAction(m_sa_panel)
        m_sa_panel.triggered.connect(lambda: self.m_spectrumAnalyzer.show())
        m_sg_panel = QAction("Signal generator", self)
        m_toolbars.addAction(m_sg_panel)
        m_toolbars.setMovable(False)
        m_toolbars.addSeparator()
        m_sg_panel.triggered.connect(lambda: self.m_signalGenerator.show())

        main_layout = QGridLayout()
        main_layout.addWidget(m_toolbars)
        main_layout.addWidget(self.txGroupBox, 1, 0)
        main_layout.addWidget(self.rxGroupBox, 1, 1)
        self.setLayout(main_layout)

    """ delete objects on closing in destructor """

    def closeEvent(self, event):
        del self.m_serialPort  # close serial ports if open
        del self.m_spectrumAnalyzer
        del self.m_signalGenerator

    '''  Create Tx management Box        '''

    def createTxBox(self):
        m_txFormLayout = QFormLayout(self.m_txContainerWidget)

        m_scanPort = QPushButton("Scan", self.m_txContainerWidget)
        m_portHBox = QHBoxLayout(self.m_txContainerWidget)
        m_portHBox.addWidget(m_scanPort)
        m_portHBox.addWidget(self.m_port)
        m_txFormLayout.addRow(m_portHBox)
        m_txConnectDisconnectHBox = QHBoxLayout(self.m_txContainerWidget)
        m_txConnectDisconnectHBox.addWidget(self.m_connectPort)
        m_txConnectDisconnectHBox.addWidget(self.m_disconnectPort)
        m_txFormLayout.addRow(m_txConnectDisconnectHBox)

        self.m_txMod.insertItem(0, "SSN_FSK_100")  # 300KHz spacing
        self.m_txMod.insertItem(1, "SSN_FSK_150")
        self.m_txMod.insertItem(2, "SSN_GFSK_150")  # 300KHz spacing
        self.m_txMod.insertItem(3, "SSN_GFSK_200")
        self.m_txMod.insertItem(4, "SSN_GFSK_300")
        self.m_txMod.insertItem(5, "MRFSK150")
        self.m_txMod.insertItem(6, "OFDM_OPT1_MCS4")  # 1200KHz spacing
        self.m_txMod.insertItem(7, "OFDM_OPT1_MCS6")  # 1200KHz spacing
        self.m_txMod.insertItem(8, "OFDM_OPT3_MCS3")
        self.m_txMod.insertItem(9, "OFDM_OPT3_MCS6")
        self.m_txMod.insertItem(10, "OQPSK12.5")
        m_txFormLayout.addRow("Modulation", self.m_txMod)

        self.psdulen.insert("32")
        self.psdulen.setEnabled(False)
        m_txFormLayout.addRow("Packet length (B)", self.psdulen)

        self.m_txFreq.insert("902")
        m_txFormLayout.addRow("Frequency (MHz)", self.m_txFreq)

        for i in range(61):
            self.m_txPower.insertItem(i, str(i) + "*0.5")
        self.m_txPower.setCurrentIndex(25)
        m_txFormLayout.addRow("Power(dBm)", self.m_txPower)

        self.m_numOfPacket.insert("1")
        self.m_numOfPacket.setEnabled(False)
        m_txFormLayout.addRow("Number of packets", self.m_numOfPacket)

        self.m_gap.insert("100")
        self.m_gap.setEnabled(False)
        m_txFormLayout.addRow("Gap (ms)", self.m_gap)

        m_loopEnableBox = QHBoxLayout(self.m_txContainerWidget)
        m_loopEnableBox.addWidget(self.m_txLoopEnable)
        m_loopEnableBox.addWidget(self.m_txFreqOffsetEnable)
        m_txFormLayout.addRow(m_loopEnableBox)

        self.m_txFreqStop.insert("928")
        m_txFormLayout.addRow("Stop Frequency (MHz)", self.m_txFreqStop)
        self.m_txFreqStep.insert("1")
        m_txFormLayout.addRow("Frequency step (MHz)", self.m_txFreqStep)
        for i in range(59):
            self.m_txPowerStop.insertItem(i, str(i) + "*0.5")
        self.m_txPowerStop.setCurrentIndex(25)
        m_txFormLayout.addRow("Stop Power (dBm)", self.m_txPowerStop)
        for i in range(6):
            self.m_txPowerStep.insertItem(i, str(1 << i) + "*0.5")
        m_txFormLayout.addRow("Power Step (dB)", self.m_txPowerStep)
        self.m_txFreqStop.setEnabled(False)
        self.m_txFreqStep.setEnabled(False)
        self.m_txPowerStop.setEnabled(False)
        self.m_txPowerStep.setEnabled(False)

        m_testModeHBox1 = QHBoxLayout(self.m_txContainerWidget)
        self.m_testMode.setChecked(True)
        m_testModeHBox1.addWidget(self.m_testMode)
        m_testModeHBox1.addWidget(self.m_levelSet)
        m_txFormLayout.addRow(m_testModeHBox1)

        for i in range(12):
            self.m_RFIC.insertItem(i, str(3 * i))
        m_txFormLayout.addRow("RFIC (dB)", self.m_RFIC)

        self.m_DMCC.insert("16383")
        m_txFormLayout.addRow("DMCC", self.m_DMCC)

        m_testModeHBox2 = QHBoxLayout(self.m_txContainerWidget)
        m_testModeHBox2.addWidget(self.m_txContinuous)
        m_testModeHBox2.addWidget(self.m_txCW)
        m_txFormLayout.addRow(m_testModeHBox2)

        for i in range(2):
            self.m_ant.insertItem(i, str(i))
        m_txFormLayout.addRow("ANT", self.m_ant)

        self.m_levelSet.setEnabled(False)
        self.m_RFIC.setEnabled(False)
        self.m_DMCC.setEnabled(False)
        self.m_ant.setEnabled(False)

        self.m_txStart.setEnabled(False)
        self.m_txStop.setEnabled(False)
        m_startStopTxHBox = QHBoxLayout(self.m_txContainerWidget)
        m_startStopTxHBox.addWidget(self.m_txStart)
        m_startStopTxHBox.addWidget(self.m_txStop)
        m_txFormLayout.addRow(m_startStopTxHBox)

        self.m_txACLR.setEnabled(False)
        m_txFormLayout.addRow(self.m_txACLR)

        self.txGroupBox.setLayout(m_txFormLayout)

        self.m_serialPort.slot_listPorts(self)  # scan ports on opening

        m_scanPort.clicked.connect(lambda: self.m_serialPort.slot_listPorts(self))
        self.m_connectPort.clicked.connect(lambda: self.m_serialPort.slot_openUart(self))
        self.m_disconnectPort.clicked.connect(lambda: self.m_serialPort.slot_closeUart(self))
        self.m_txLoopEnable.stateChanged.connect(lambda: self.slot_txLoopEnable())
        self.m_testMode.stateChanged.connect(lambda: self.slot_txTestModeEnable())
        self.m_txStart.clicked.connect(lambda: self.m_serialPort.slot_startTx(self, self.m_spectrumAnalyzer))
        self.m_txStop.clicked.connect(lambda: self.m_serialPort.slot_stopTx())
        self.m_txACLR.clicked.connect(lambda: self.m_serialPort.slot_startACLR(self, self.m_spectrumAnalyzer))
        
    '''  Create Rx management Box        '''

    def createRxBox(self):
        m_rxFormLayout = QFormLayout(self.m_rxContainerWidget)

        self.m_rxFreq.insert("902")
        m_rxFormLayout.addRow("Frequency (MHz)", self.m_rxFreq)

        m_loopEnableBox = QHBoxLayout(self.m_rxContainerWidget)
        m_loopEnableBox.addWidget(self.m_rxLoopEnable)
        m_loopEnableBox.addWidget(self.m_rxTestMode)
        m_rxFormLayout.addRow(m_loopEnableBox)

        self.m_rxFreqStop.insert("928")
        m_rxFormLayout.addRow("Stop Frequency (MHz)", self.m_rxFreqStop)
        self.m_rxFreqStep.insert("1")
        m_rxFormLayout.addRow("Frequency step (MHz)", self.m_rxFreqStep)
        self.m_rxPowerStart.insert("-100")
        m_rxFormLayout.addRow("Start Power (dBm)", self.m_rxPowerStart)
        self.m_rxPowerStop.insert("0")
        m_rxFormLayout.addRow("Stop Power (dBm)", self.m_rxPowerStop)
        self.m_rxPowerStep.insert("10")
        m_rxFormLayout.addRow("Step Power (dBm)", self.m_rxPowerStep)
        self.m_cableLoss.insert("12")
        m_rxFormLayout.addRow("Cable Loss (dB)", self.m_cableLoss)
        self.m_rxFreqStop.setEnabled(False)
        self.m_rxFreqStep.setEnabled(False)
        self.m_rxPowerStart.setEnabled(False)
        self.m_rxPowerStop.setEnabled(False)
        self.m_rxPowerStep.setEnabled(False)
        self.m_cableLoss.setEnabled(False)

        self.m_rssiRequest.setEnabled(False)
        m_RSSIHBox = QHBoxLayout(self.m_rxContainerWidget)
        m_RSSIHBox.addWidget(self.m_rssiRequest)
        m_RSSIHBox.addWidget(self.m_rssi)
        m_rxFormLayout.addRow(m_RSSIHBox)

        self.m_rxConfig.setEnabled(False)
        m_rxFormLayout.addRow(self.m_rxConfig)

        self.m_fskCounter.insert("0")
        self.m_fskCounter.setEnabled(False)
        m_rxFormLayout.addRow("FSK", self.m_fskCounter)
        self.m_ofdmCounter.insert("0")
        self.m_ofdmCounter.setEnabled(False)
        m_rxFormLayout.addRow("OFDM", self.m_ofdmCounter)
        self.m_oqpskCounter.insert("0")
        self.m_oqpskCounter.setEnabled(False)
        m_rxFormLayout.addRow("OQPSK", self.m_oqpskCounter)
        self.m_pkt_rssi.insert("0")
        self.m_pkt_rssi.setEnabled(False)
        m_rxFormLayout.addRow("RSSI", self.m_pkt_rssi)

        self.m_FSK150k.setChecked(True)

        m_modHBox1 = QHBoxLayout(self.m_rxContainerWidget)
        m_modHBox1.addWidget(self.m_FSK150k)
        m_modHBox1.addWidget(self.m_OFDM200k)
        m_modHBox1.addWidget(self.m_OFDM600k)
        m_rxFormLayout.addRow(m_modHBox1)

        m_modHBox2 = QHBoxLayout(self.m_rxContainerWidget)
        m_modHBox2.addWidget(self.m_LR125k)
        m_modHBox2.addWidget(self.m_SSNFSK100k)
        m_modHBox2.addWidget(self.m_SSNFSK150k)
        m_rxFormLayout.addRow(m_modHBox2)

        m_modHBox3 = QHBoxLayout(self.m_rxContainerWidget)
        m_modHBox3.addWidget(self.m_SSNGFSK150k)
        m_modHBox3.addWidget(self.m_SSNGFSK200k)
        m_modHBox3.addWidget(self.m_SSNGFSK300k)
        m_rxFormLayout.addRow(m_modHBox3)

        m_modHBox4 = QHBoxLayout(self.m_rxContainerWidget)
        m_modHBox4.addWidget(self.m_OFDM1200k)
        m_modHBox4.addWidget(self.m_OFDM2400k)
        m_rxFormLayout.addRow(m_modHBox4)

        self.m_packets.insert("100")
        m_rxFormLayout.addRow("Packets", self.m_packets)

        m_rxFormLayout.addRow(self.m_sensitivity)
        self.m_sensitivity.setEnabled(False)
        m_rxFormLayout.addRow(self.m_rssiSweep)
        self.m_rssiSweep.setEnabled(False)

        self.rxGroupBox.setLayout(m_rxFormLayout)

        self.m_rxConfig.clicked.connect(lambda: self.m_serialPort.slot_rx(self, self.m_signalGenerator))
        self.m_rssiRequest.clicked.connect(lambda: self.m_serialPort.slot_rssiReq())
        self.m_rxLoopEnable.stateChanged.connect(lambda: self.slot_rxLoopEnable())
        self.m_sensitivity.clicked.connect(lambda: self.m_serialPort.slot_sensitivity(self, self.m_signalGenerator))
        self.m_rssiSweep.clicked.connect(lambda: self.m_serialPort.slot_rssi_sweep(self, self.m_signalGenerator))

    """ enable the tx test mode section only when selected"""

    def slot_txTestModeEnable(self):
        if self.m_testMode.isChecked():
            self.m_levelSet.setEnabled(True)
            self.m_RFIC.setEnabled(True)
            self.m_DMCC.setEnabled(True)
            self.m_txContinuous.setEnabled(True)
            self.m_txCW.setEnabled(True)
            self.m_ant.setEnabled(True)
        else:
            self.m_levelSet.setEnabled(False)
            self.m_RFIC.setEnabled(False)
            self.m_DMCC.setEnabled(False)
            self.m_txContinuous.setEnabled(False)
            self.m_txCW.setEnabled(False)
            self.m_ant.setEnabled(False)

    """ Enable the tx loop test section only when selected """

    def slot_txLoopEnable(self):
        if self.m_txLoopEnable.isChecked():
            self.m_txFreqStop.setEnabled(True)
            self.m_txFreqStep.setEnabled(True)
            self.m_testMode.setChecked(True)
            self.m_txPowerStop.setEnabled(True)
            self.m_txPowerStep.setEnabled(True)
            self.m_txCW.setChecked(True)
            self.m_txACLR.setEnabled(True)
        else:
            self.m_txFreqStop.setEnabled(False)
            self.m_txFreqStep.setEnabled(False)
            self.m_testMode.setChecked(False)
            self.m_txPowerStop.setEnabled(False)
            self.m_txPowerStep.setEnabled(False)
            self.m_txCW.setChecked(False)
            self.m_txACLR.setEnabled(False)

    def slot_rxLoopEnable(self):
        if self.m_rxLoopEnable.isChecked():
            self.m_rxFreqStop.setEnabled(True)
            self.m_rxFreqStep.setEnabled(True)
            self.m_rxPowerStart.setEnabled(True)
            self.m_rxPowerStop.setEnabled(True)
            self.m_rxPowerStep.setEnabled(True)
            self.m_cableLoss.setEnabled(True)
        else:
            self.m_rxFreqStop.setEnabled(False)
            self.m_rxFreqStep.setEnabled(False)
            self.m_rxPowerStart.setEnabled(False)
            self.m_rxPowerStop.setEnabled(False)
            self.m_rxPowerStep.setEnabled(False)
            self.m_cableLoss.setEnabled(False)
