import visa
from PyQt5.QtWidgets import (QCheckBox, QComboBox, QDialog, QFormLayout, QGroupBox, QHBoxLayout, QLineEdit, QPushButton,
                             QVBoxLayout, QWidget)


class rotator(QDialog):
    def __init__(self):
        super().__init__()
        self.rm = visa.ResourceManager()
        self.rm.list_resources()

        self.setWindowTitle("Rotator")
        containerWidget = QWidget(self)
        formLayout = QFormLayout(containerWidget)

        self.address = QLineEdit(containerWidget)
        self.address.insert("GPIB1::11::INSTR")
        formLayout.addRow("Address 1", self.address)
        self.address1 = QLineEdit(containerWidget)
        self.address1.insert("GPIB1::12::INSTR")
        formLayout.addRow("Address 2", self.address1)
        self.m_connect = QPushButton("Connect", containerWidget)
        formLayout.addRow(self.m_connect)

        self.theta = QLineEdit(containerWidget)
        self.theta.insert("0")
        formLayout.addRow("Theta", self.theta)
        self.phi = QLineEdit(containerWidget)
        self.phi.insert("0")
        formLayout.addRow("Phi", self.phi)

        self.groupBox = QGroupBox("Rotator", self)
        self.groupBox.setLayout(formLayout)
        layout = QVBoxLayout()
        layout.addWidget(self.groupBox)
        self.setLayout(layout)

        self.m_connect.clicked.connect(lambda: self.connect())
        self.theta.editingFinished.connect(lambda: self.goto_theta(self.theta.text()))
        self.phi.editingFinished.connect(lambda: self.goto_phi(self.phi.text()))

    def connect(self):
        address = self.address.text()
        address1 = self.address1.text()
        try:
            self.r = self.rm.open_resource(address)
            print("Connected to " + self.r.query('*IDN?'))
            self.r1 = self.rm.open_resource(address1)
            print("Connected to " + self.r1.query('*IDN?'))
        except:
            print("Connection error!")
            return -1

    def goto_theta(self, loc):
        self.r.write("GOTO " + str(loc))

    def goto_phi(self, loc):
        self.r1.write("GOTO " + str(loc % 360))

    def theta_busy(self):
        return self.r.query("*STB?") & ~self.r.query("*OPC?") & 1

    def phi_busy(self):
        return self.r1.query("*STB?") & ~self.r1.query("*OPC?") & 1
