# -*- coding: utf-8 -*-

import json, os, random

from .ConnectDialog import Ui_ConnectDialog
from .ConnectToDialog import Ui_ConnectToDialog
from .EditConnectionDialog import Ui_EditConnectionDialog

import PyQt5
from PyQt5.QtWidgets import \
	QApplication, QMainWindow, QSystemTrayIcon, QMenu, \
	QAction, QWidget, QStyle, QDialog, QMessageBox, \
	QListWidgetItem, QToolBar, QLineEdit
from PyQt5.QtNetwork import QHostAddress

from PyQt5 import QtGui, QtCore, QtWidgets



def get_random_ip():
	ip1 = random.randint(0,200)
	ip2 = random.randint(0,200)
	return "10.5." + str(ip1) + "." + str(ip2)


class ConnectToDialog(QDialog, Ui_ConnectToDialog):
	
	def __init__(self):
		QDialog.__init__(self)
		self.setupUi(self)
		self.label.setWordWrap(True)
		self.setFixedSize(self.size())
	

class EditConnectionDialog(QDialog, Ui_EditConnectionDialog):
	
	def __init__(self):
		QDialog.__init__(self)
		self.setupUi(self)
		self.setFixedSize(self.size())
		
		# Set default value
		self.enableRelay.setChecked(True)
		self.autoStartPeerVPN.setChecked(True)
		
		# Setup random IP
		ip = get_random_ip()
		self.localIpEdit.setText( ip )


class Connection():
	
	def __init__(self):
		self.user_name = ""
		self.connection_name = "";
		self.secret_key = "";
		self.connection_string = ""
		self.client_port = 0
		self.enable_relay = False
		self.local_ip = ""
		self.auto_start_vpn = True
		self.vpn_version = "32bit"
		
		
	def fromObj(self, obj):
		
		try:
			self.user_name = obj["user_name"]
		except Exception as e:
			pass
		
		try:
			self.connection_name = obj["connection_name"]
		except Exception as e:
			pass
		
		try:
			self.secret_key = obj["secret_key"]
		except Exception as e:
			pass
		
		try:
			self.connection_string = obj["connection_string"]
		except Exception as e:
			pass
			
		try:
			self.client_port = int(obj["client_port"])
		except Exception as e:
			pass
		
		try:
			enable_relay = int(obj["enable_relay"])
			if enable_relay != 0:
				self.enable_relay = True
			else:
				self.enable_relay = False
		except Exception as e:
			pass
		
		try:
			auto_start_vpn = int(obj["auto_start_vpn"])
			if auto_start_vpn != 0:
				self.auto_start_vpn = True
			else:
				self.auto_start_vpn = False
		except Exception as e:
			pass
		
		try:
			self.local_ip = obj["local_ip"]
		except Exception as e:
			pass
		
		try:
			self.vpn_version = obj["vpn_version"]
		except Exception as e:
			pass
		
		if self.local_ip == "":
			self.local_ip = get_random_ip()
		
	
	def toObj(self):
		obj = {
			"user_name": self.user_name,
			"connection_name": self.connection_name,
			"secret_key": self.secret_key,
			"connection_string": self.connection_string,
			"local_ip": self.local_ip,
			"vpn_version": self.vpn_version,
		}
		
		try:
			obj["client_port"] = int(self.client_port)
		except Exception as e:
			pass
		
		if self.enable_relay:
			obj["enable_relay"] = 1
		else:
			obj["enable_relay"] = 0
		
		if self.auto_start_vpn:
			obj["auto_start_vpn"] = 1
		else:
			obj["auto_start_vpn"] = 0
		
		return obj
	
	
	def setupDialog(self, dlg:EditConnectionDialog):
		dlg.userNameEdit.setText( self.user_name )
		dlg.connectionNameEdit.setText( self.connection_name )
		dlg.secretKeyEdit.setText( self.secret_key )
		dlg.connectStringEdit.setText( self.connection_string )
		dlg.clientPortEdit.setText( str(self.client_port) )
		dlg.localIpEdit.setText( self.local_ip )
		
		if self.auto_start_vpn:
			dlg.autoStartPeerVPN.setChecked(True)
		else:
			dlg.autoStartPeerVPN.setChecked(False)
		
		if self.enable_relay:
			dlg.enableRelay.setChecked(True)
		else:
			dlg.enableRelay.setChecked(False)
		
		if self.vpn_version == "32bit":
			dlg.vpnVersion.setCurrentIndex(0)
		else:
			dlg.vpnVersion.setCurrentIndex(1)
	
	
	def readDialog(self, dlg:EditConnectionDialog):
		self.user_name = dlg.userNameEdit.text()
		self.connection_name = dlg.connectionNameEdit.text()
		self.secret_key = dlg.secretKeyEdit.text()
		self.connection_string = dlg.connectStringEdit.text()
		self.local_ip = dlg.localIpEdit.text()
		self.vpn_version = dlg.vpnVersion.currentText()
		
		try:
			self.client_port = int( dlg.clientPortEdit.text() )
		except Exception as e:
			pass
		
		if dlg.autoStartPeerVPN.isChecked():
			self.auto_start_vpn = True
		else:
			self.auto_start_vpn = False
		
		if dlg.enableRelay.isChecked():
			self.enable_relay = True
		else:
			self.enable_relay = False
		
	
	def getConnectionList(self):
		
		items = self.connection_string.split(";")
		res = []
		
		for index in range(len(items)):
			item = items[index]
			arr = item.split(":")
			
			try:
				ip = QHostAddress(arr[0])
				port = int(arr[1])
				
				if ip.toString() == arr[0] and port != 0:
					res.append( (ip, port) )
				
			except Exception as e:
				pass
		
		
		return res
	

class ConnectDialog(QDialog, Ui_ConnectDialog):
	
	def __init__(self):
		QDialog.__init__(self)
		self.setupUi(self)
		self.setFixedSize(self.size())
		self.listWidget.setSortingEnabled(True)
		
		# Selected connection
		self.connection = None
		
		# Actions
		self.addButton.clicked.connect(self.onAddClick)
		self.editButton.clicked.connect(self.onEditClick)
		self.deleteButton.clicked.connect(self.onDeleteClick)
		self.connectButton.clicked.connect(self.onConnectClick)
		
		# Load items
		self.loadItems()
		
	
	def getSettingsFileName(self):
		path = os.path.expanduser('~')
		path = os.path.join(path, ".config", "p2p_chat")
		os.makedirs(path, exist_ok=True)
		file_name = os.path.join(path, "settings.json")
		return file_name
	
	
	def loadItems(self):
		
		file_name = self.getSettingsFileName()
		file_content = ""
		
		try:
			if os.path.exists(file_name):
				with open(file_name) as file:
					file_content = file.read()
					file.close()
				
				settings = json.loads(file_content)
				connections = settings["connections"]
				
				for obj in connections:
					connection = Connection()
					connection.fromObj(obj)
					item = QListWidgetItem(connection.connection_name)
					item.setData(1, connection)
					self.listWidget.addItem(item)
				
		finally:
			pass
		
		pass
	
	
	def saveItems(self):
		
		connections = []
		for row in range(self.listWidget.count()):
			item = self.listWidget.item(row)
			connection = item.data(1)
			obj = connection.toObj()
			connections.append(obj)
		
		settings = {
			"connections": connections
		}
		
		text = json.dumps(settings, indent=2) 
		
		file_name = self.getSettingsFileName()
		with open(file_name, "w") as file:
			file.write(text)
			file.close()
			
		pass
	
	
	def onAddClick(self):
		self.show_edit_connection_dialog()
		self.saveItems()
	
	
	def onEditClick(self):
		
		items = self.listWidget.selectedIndexes()
		if len(items) > 0:
			self.show_edit_connection_dialog( self.listWidget.item(items[0].row()) )
			
		self.saveItems()
	
	
	def onDeleteClick(self):
		
		delete_msg = "Are you sure want to delete selected items?"
		result = QMessageBox.question(self, "Delete selected items",
				delete_msg, QMessageBox.Yes, QMessageBox.No)
		
		if result == QMessageBox.Yes:
			items = self.listWidget.selectedIndexes()
			for item in items:
				row = item.row()
				self.listWidget.takeItem(row)
			
			self.saveItems()
	
	
	def show_edit_connection_dialog(self, item:QListWidgetItem = None):
		dlg = EditConnectionDialog()
		
		if item != None:
			connection = item.data(1)
			connection.setupDialog(dlg)
		
		result = dlg.exec()
		
		if result == 1:
			
			# Create data
			connection = Connection()
			connection.readDialog(dlg)
			
			# Add data to list widget
			if item == None:
				item = QListWidgetItem(connection.connection_name)
				item.setData(1, connection)
				self.listWidget.addItem(item)
			
			else:
				item.setText(connection.connection_name)
				item.setData(1, connection)
				
				
	def onConnectClick(self):
		
		items = self.listWidget.selectedIndexes()
		if len(items) > 0:
			row = items[0].row()
			item = self.listWidget.item(row)
			connection = item.data(1)
			self.connection = connection
		
		self.close()
		
		pass