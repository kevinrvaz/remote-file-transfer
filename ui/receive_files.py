# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'receive_files.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(689, 631)
        Dialog.setStyleSheet("#Dialog {\n"
"    background-color: white;\n"
"}")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 641, 61))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.label.setFont(font)
        self.label.setStyleSheet("#label {\n"
"    font-size: 40px;\n"
"}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(50, 160, 595, 431))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setStyleSheet("#label_2 {\n"
"    font-size: 20px;\n"
"}")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.lineEditIP = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEditIP.setStyleSheet("#lineEditIP {\n"
"    margin: 5px auto;\n"
"    padding: 5px auto;\n"
"}")
        self.lineEditIP.setObjectName("lineEditIP")
        self.horizontalLayout.addWidget(self.lineEditIP)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_3.setStyleSheet("#label_3 {\n"
"    font-size: 20px;\n"
"}")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.lineEditSavePath = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEditSavePath.setStyleSheet("#lineEditSavePath {\n"
"    margin: 10px auto;\n"
"    padding: 5px auto;\n"
"}")
        self.lineEditSavePath.setObjectName("lineEditSavePath")
        self.horizontalLayout_2.addWidget(self.lineEditSavePath)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.receiveButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.receiveButton.setStyleSheet("#receiveButton {\n"
"    font-size: 20px;\n"
"    background-color: white;\n"
"    color: red;\n"
"    border: 2px solid red;\n"
"    border-radius: 10px;\n"
"    padding: 10px auto;\n"
"    margin: 20px 200px;\n"
"}\n"
"\n"
"#receiveButton:hover {\n"
"    background-color: red;\n"
"    color: white;\n"
"}")
        self.receiveButton.setObjectName("receiveButton")
        self.verticalLayout.addWidget(self.receiveButton)
        self.label_4 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_4.setStyleSheet("#label_4 {\n"
"    font-size: 20px;\n"
"    color: green;\n"
"}")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setStyleSheet("")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Remote File Sharing"))
        self.label_2.setText(_translate("Dialog", "Sender IPv4 address"))
        self.label_3.setText(_translate("Dialog", "Save Path (absolute)"))
        self.receiveButton.setText(_translate("Dialog", "Receive Files"))
        self.label_4.setText(_translate("Dialog", "Download in progress"))
