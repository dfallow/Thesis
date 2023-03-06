import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QStackedWidget, QMainWindow, QListView, QListWidgetItem
from pythonScripts.machineSetup import registerMachine
from pythonScripts.getDevices import getDevices


class MainScreen(QMainWindow):
    def __init__(self):
        super(MainScreen, self).__init__()
        loadUi("main.ui", self)
        self.btn_go_to_register.clicked.connect(self.gotoregister)
        self.btn_go_to_devices.clicked.connect(self.gotodevices)

    def gotoregister(self):
        register = RegisterScreen()
        widget.addWidget(register)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def gotodevices(self):
        devices = AllDevicesScreen()
        widget.addWidget(devices)
        widget.setCurrentIndex(widget.currentIndex()+2)



class RegisterScreen(QMainWindow):
    def __init__(self):
        super(RegisterScreen, self).__init__()
        loadUi("registerDevice.ui", self)
        self.input_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btn_register.clicked.connect(self.registerfunction)

    def registerfunction(self):
        address = self.input_address.text()
        user = self.input_username.text()
        password = self.input_password.text()
        device_name = self.input_name.text()
        print(user + password)

        registerMachine(address, user, password, device_name)

class AllDevicesScreen(QMainWindow):
    def __init__(self):
        super(AllDevicesScreen, self).__init__()
        loadUi("allDevices.ui", self)
        self.btn_refresh.clicked.connect(self.getAllDevices)

    def getAllDevices(self):
        devices = getDevices()
        print(devices)

        self.list_devices.addItems(devices)
        
            




# main
app = QApplication(sys.argv)
main = MainScreen()
widget = QStackedWidget()
widget.addWidget(main)
widget.setFixedHeight(600)
widget.setFixedWidth(800)
widget.show()
try:
    sys.exit(app.exec())
except:
    print("Exiting")