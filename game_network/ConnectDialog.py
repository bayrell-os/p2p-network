# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/drive/d/files/Projects/bayrell/p2p-network/p2p_network/ConnectDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ConnectDialog(object):
    def setupUi(self, ConnectDialog):
        ConnectDialog.setObjectName("ConnectDialog")
        ConnectDialog.resize(544, 394)
        self.centralwidget = QtWidgets.QWidget(ConnectDialog)
        self.centralwidget.setGeometry(QtCore.QRect(0, 0, 537, 391))
        self.centralwidget.setObjectName("centralwidget")
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setGeometry(QtCore.QRect(440, 20, 97, 33))
        self.addButton.setObjectName("addButton")
        self.deleteButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(440, 100, 97, 33))
        self.deleteButton.setObjectName("deleteButton")
        self.editButton = QtWidgets.QPushButton(self.centralwidget)
        self.editButton.setGeometry(QtCore.QRect(440, 60, 97, 33))
        self.editButton.setObjectName("editButton")
        self.connectButton = QtWidgets.QPushButton(self.centralwidget)
        self.connectButton.setGeometry(QtCore.QRect(440, 190, 97, 33))
        self.connectButton.setObjectName("connectButton")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 0, 431, 391))
        self.listWidget.setObjectName("listWidget")

        self.retranslateUi(ConnectDialog)
        QtCore.QMetaObject.connectSlotsByName(ConnectDialog)

    def retranslateUi(self, ConnectDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectDialog.setWindowTitle(_translate("ConnectDialog", "Connect"))
        self.addButton.setText(_translate("ConnectDialog", "Add"))
        self.deleteButton.setText(_translate("ConnectDialog", "Delete"))
        self.editButton.setText(_translate("ConnectDialog", "Edit"))
        self.connectButton.setText(_translate("ConnectDialog", "Connect"))
        self.listWidget.setSortingEnabled(True)
