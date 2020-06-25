import datetime
import math
import time
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
            m_mainWindow.m_start.setEnabled(True)
            m_mainWindow.m_stop.setEnabled(True)
        except:
            print("Error!?")

    def slot_closeUart(self, m_mainWindow):
        try:
            self.m_serialPort.close()
            print("Disconnected from " + m_mainWindow.m_port.currentText())
            m_mainWindow.m_connectPort.setEnabled(True)
            m_mainWindow.m_disconnectPort.setEnabled(False)
            m_mainWindow.m_start.setEnabled(False)
            m_mainWindow.m_stop.setEnabled(False)
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

    def vertical(self, i):
        self.m_serialPort.rts = i

