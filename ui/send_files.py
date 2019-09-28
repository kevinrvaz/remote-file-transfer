# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'send_files.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(665, 627)
        Dialog.setStyleSheet("#Dialog {\n"
"    background-color: white;\n"
"}")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 160, 624, 411))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.genIP = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.genIP.setStyleSheet("#genIP {\n"
"    font-size: 20px;\n"
"    color: red;\n"
"    border: 2px solid red;\n"
"    background-color: white;\n"
"    padding: 10px auto;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#genIP:hover {\n"
"    background-color: red;\n"
"    color: white;\n"
"}")
        self.genIP.setObjectName("genIP")
        self.horizontalLayout.addWidget(self.genIP)
        self.ipLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.ipLabel.setStyleSheet("#ipLabel {\n"
"    font-size: 20px;\n"
"}")
        self.ipLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ipLabel.setObjectName("ipLabel")
        self.horizontalLayout.addWidget(self.ipLabel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelFileLocation = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.labelFileLocation.setStyleSheet("#labelFileLocation {\n"
"    font-size: 20px;\n"
"}")
        self.labelFileLocation.setObjectName("labelFileLocation")
        self.horizontalLayout_2.addWidget(self.labelFileLocation)
        self.lineEditFileLocation = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEditFileLocation.setStyleSheet("#lineEditFileLocation {\n"
"    margin: 5px auto;\n"
"    padding: 5px auto;\n"
"}")
        self.lineEditFileLocation.setObjectName("lineEditFileLocation")
        self.horizontalLayout_2.addWidget(self.lineEditFileLocation)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.sendButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.sendButton.setStyleSheet("#sendButton {\n"
"    margin: 20px 200px;\n"
"    background-color: white;\n"
"    color: blue;\n"
"    padding: 10px auto;\n"
"    border: 2px solid blue;\n"
"    border-radius: 10px;\n"
"    font-size: 20px;\n"
"}\n"
"\n"
"#sendButton:hover {\n"
"    color: white;\n"
"    background-color: blue;\n"
"}")
        self.sendButton.setObjectName("sendButton")
        self.verticalLayout.addWidget(self.sendButton)
        self.labelProgress = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.labelProgress.setStyleSheet("#labelProgress {\n"
"    font-size: 20px;\n"
"    color: green;\n"
"    background-color: white;\n"
"}")
        self.labelProgress.setAlignment(QtCore.Qt.AlignCenter)
        self.labelProgress.setObjectName("labelProgress")
        self.verticalLayout.addWidget(self.labelProgress)
        self.progressBar = QtWidgets.QProgressBar(self.verticalLayoutWidget)
        self.progressBar.setStyleSheet("")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 50, 641, 61))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.label.setFont(font)
        self.label.setStyleSheet("#label {\n"
"    font-size: 40px;\n"
"}")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Send Files"))
        self.genIP.setToolTip(_translate("Dialog", "Click to generate an ip to share with the receiver"))
        self.genIP.setText(_translate("Dialog", "Generate IPv4 address"))
        self.ipLabel.setText(_translate("Dialog", "e.g. 127.0.0.1"))
        self.labelFileLocation.setText(_translate("Dialog", "Enter File Location"))
        self.lineEditFileLocation.setToolTip(_translate("Dialog", "Enter the absolute path of the file to be transfered, incase of multiple files share the location of the compressed file."))
        self.sendButton.setToolTip(_translate("Dialog", "Begin transmission of files to the receiver"))
        self.sendButton.setText(_translate("Dialog", "Send"))
        self.labelProgress.setText(_translate("Dialog", "Transfer Progress"))
        self.label.setText(_translate("Dialog", "Remote File Sharing"))
