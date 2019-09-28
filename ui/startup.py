# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'startup.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 480)
        Dialog.setStyleSheet("#Dialog {\n"
"    margin: 0 auto;\n"
"    padding: 0 auto;\n"
"    background-color: white;\n"
"}")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(169, 170, 301, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sendFiles = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.sendFiles.setFont(font)
        self.sendFiles.setStyleSheet("#sendFiles {\n"
"    background-color: white;\n"
"    font-size: 20px;\n"
"    color: blue;\n"
"    padding: 10px auto;\n"
"    border: 2px solid blue;\n"
"    border-radius: 10px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"#sendFiles:hover {\n"
"    color: white;\n"
"    background-color: blue;\n"
"}")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("assets/upload-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sendFiles.setIcon(icon)
        self.sendFiles.setIconSize(QtCore.QSize(24, 24))
        self.sendFiles.setFlat(True)
        self.sendFiles.setObjectName("sendFiles")
        self.verticalLayout.addWidget(self.sendFiles)
        self.receiveFiles = QtWidgets.QPushButton(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.receiveFiles.setFont(font)
        self.receiveFiles.setStyleSheet("#receiveFiles {\n"
"    background-color: white;\n"
"    padding: 10px auto;\n"
"    font-size: 20px;\n"
"    color: red;\n"
"    border: 2px solid red;\n"
"    border-radius: 10px;\n"
"}\n"
"\n"
"#receiveFiles:hover {\n"
"    background-color: red;\n"
"    color: white;\n"
"}")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("assets/download-solid.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.receiveFiles.setIcon(icon1)
        self.receiveFiles.setIconSize(QtCore.QSize(24, 24))
        self.receiveFiles.setObjectName("receiveFiles")
        self.verticalLayout.addWidget(self.receiveFiles)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 60, 641, 61))
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
        Dialog.setWindowTitle(_translate("Dialog", "Remote Files Sharing"))
        self.sendFiles.setText(_translate("Dialog", " Send Files"))
        self.receiveFiles.setText(_translate("Dialog", " Receive Files"))
        self.label.setText(_translate("Dialog", "Remote File Sharing"))
import icons_rc
