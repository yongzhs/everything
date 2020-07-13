from PyQt5.QtWidgets import QApplication

import mainWindow
import sys

if __name__ == '__main__':
    def run_app():
        app = QApplication(sys.argv)
        window = mainWindow.MainWindow()
        window.show()
        app.exec_()


    run_app()