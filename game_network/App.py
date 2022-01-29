# -*- coding: utf-8 -*-

import sys, threading, time, base64, json, hashlib, os, io

from PyQt5 import QtNetwork
from PyQt5.sip import enableoverflowchecking

from .AboutDialog import Ui_AboutDialog
from .MainWindow import Ui_MainWindow
from .LogWindow import Ui_LogWindow
from .Connect import Connection, ConnectDialog, ConnectToDialog
from .Helper import Helper

import PyQt5
from PyQt5.QtWidgets import \
	QApplication, QMainWindow, QSystemTrayIcon, QMenu, \
	QAction, QWidget, QStyle, QDialog, QMessageBox, \
	QListWidgetItem, QToolBar, QLineEdit, QMenuBar, QMenu, \
	QTextBrowser, QTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, QUrl, QTime, QDate
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtNetwork import QUdpSocket, QHostAddress
from PyQt5 import QtGui, QtCore, QtWidgets


# Принимать только те сообщения, у которых разница во времени меньше этого значения
MAX_MESSAGE_TIME = 60 * 60

# Через сколько будет отправляться пинг
PING_TIME_INTERVAL = 45
#PING_TIME_INTERVAL = 5
BROADCAST_PING_TIME_INTERVAL = 15

# Обновление списков клиентов у всех участников
UPDATE_CLIENTS_INTERVAL = int(5 * BROADCAST_PING_TIME_INTERVAL)

# Сколько времени клиент считается актуальным, если от него не приходят пинги
MAX_CLIENT_TIME = 10 * BROADCAST_PING_TIME_INTERVAL

# Через какое время удалять клиентов
REMOVE_CLIENTS_INTERVAL = int(MAX_CLIENT_TIME / 2)

# Кодировка по умолчанию
ENCODING = "utf8"

# Сколько оставлять сообщений в чате
MAX_COUNT_LINES = 1000

# Chat port
CHAT_PORT = 33001
CHAT_LOCAL = True

# PeerVPN location
PEERVPN_DIR_PATH = ""

# Main Window
main_helper = Helper()


def set_window_center(window):
	
	desktop = QApplication.desktop()
	screen_number = desktop.screenNumber(desktop.cursor().pos())
	center = desktop.screenGeometry(screen_number).center()
	
	window_size = window.size()
	width = window_size.width(); 
	height = window_size.height();
	
	x = center.x() - round(width / 2);
	y = center.y() - round(height / 2);
	
	window.move ( x, y );


def html_escape(s):
	s = s.replace("&", "&amp;")
	s = s.replace("<", "&lt;")
	s = s.replace(">", "&gt;")
	s = s.replace('"', "&quot;")
	s = s.replace('\'', "&#x27;")
	return s


def log(msg):
	main_helper.app_log(msg)
	

class AboutDialog(QDialog, Ui_AboutDialog):
	
	def __init__(self):
		QDialog.__init__(self)
		self.setupUi(self)
		self.setFixedSize(self.size())


"""
	Данные клиента. Идентификатор host:port
"""
class Client():
	
	def __init__(self):
		self.user_name = ""
		self.host = None
		self.port = 0
		self.time = 0
	
	def getClientName(self):
		host:QHostAddress = self.host
		return self.user_name + " (" + host.toString() + ")"
	


class LogWindow(QMainWindow, Ui_LogWindow):
	def __init__(self, parent=None):
		QMainWindow.__init__(self, parent)
		self.setupUi(self)
		self.clearButton.clicked.connect(self.onClearButtonClick)
		self.closeButton.clicked.connect(self.onCloseButtonClick)
	
	
	def onClearButtonClick(self):
		self.logText.clear()
	
	
	def onCloseButtonClick(self):
		self.hide()
		
		
	def show(self) -> None:
		set_window_center(self)
		return super().show()



class MainWindow(QMainWindow, Ui_MainWindow):
	
	def __init__(self):
		QMainWindow.__init__(self)
		
		# Data
		self.connection = None
		self.is_connected = False
		self.udp_socket = None
		self.is_focus = True
		
		# Set a title
		self.setupUi(self)
		self.updateTitle()
		
		# Set to center
		set_window_center(self)
		
		# Actions
		#self.sendMessageText.pressed.connect(self.onSendMessageTextPress)
		self.sendMessageButton.clicked.connect(self.onSendMessageButtonClick)
		self.actionAbout.triggered.connect(self.onAboutClick)
		self.actionConnect.triggered.connect(self.onConnectClick)
		self.actionDisconnect.triggered.connect(self.onDisconnectClick)
		self.actionQuit.triggered.connect(self.onQuitClick)
		self.actionChatLog.triggered.connect(self.onChatLogClick)
		self.actionPeerVPNLog.triggered.connect(self.onPeerVPNLogClick)
		self.actionClear.triggered.connect(self.onClearClick)
		self.actionGetYourIP.triggered.connect(self.onGetYourIPClick)
		
		# Create log window
		self.appLogWindow = LogWindow(self)
		self.appLogWindow.setWindowTitle("Chat log")
		self.peervpnLogWindow = LogWindow(self)
		self.peervpnLogWindow.setWindowTitle("PeerVPN log")
		"""
		logText:QtWidgets.QPlainTextEdit = self.appLogWindow.logText
		logText.insertPlainText("Test 1")
		logText.insertPlainText("Test 2\n aaa \n aaaaa \n      asdasdsd \r")
		logText.insertPlainText("Test 3\r")
		logText.insertPlainText("Test 4")
		#self.appLogWindow.logText.appendPlainText("Test 2")
		#self.appLogWindow.logText.appendPlainText("Test 3")
		#self.appLogWindow.logText.appendPlainText("Test 4")
		#self.appLogWindow.logText.appendPlainText("Test 5")
		"""
		pass
		
	
	"""
		Обновление заголовка окна
	"""
	def updateTitle(self):
		self.setWindowTitle("P2P Network")
		pass
	
	
	"""
		Пришло новое сообщение
	"""
	def updateNewMessageTitle(self):
		#if self.is_focus == False:
		#	self.setWindowTitle("*** New message ***")
		pass
	
	
	def onConnectClick(self):
		dlg = ConnectDialog()
		dlg.exec()
		
		if dlg.connection != None:
			self.connectToChat(dlg.connection)
			pass
	
	
	def onDisconnectClick(self):
		self.disconnectFromChat()
		
	
	def onAboutClick(self):
		dlg = AboutDialog()
		dlg.exec()
	
	
	def onQuitClick(self):
		main_helper.main_window = None
		self.close()
		sys.exit()
	
	
	def onChatLogClick(self):
		if main_helper.enable_logs:
			self.appLogWindow.show()
		pass
	
	
	def onPeerVPNLogClick(self):
		if main_helper.enable_logs:
			self.peervpnLogWindow.show()
		pass
	
	
	def onClearClick(self):
		self.chatBrowser.clear()
	
	
	def onGetYourIPClick(self):
		if self.connection != None:
			self.addNewMessage("Your Local IP: " + self.connection.local_ip)
	
	
	def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
		self.disconnectFromChat()
		main_helper.is_terminated = True
		time.sleep(0.5)
		#self.fatal_error.close()
		return super().closeEvent(a0)
	
	
	def leaveEvent(self, a0: QtCore.QEvent) -> None:
		self.is_focus = False
		return super().leaveEvent(a0)
	
	
	def enterEvent(self, a0: QtCore.QEvent) -> None:
		self.updateTitle()
		self.is_focus = True
		return super().enterEvent(a0)
	
	
	def focusInEvent(self, a0: QtGui.QFocusEvent) -> None:
		return super().focusInEvent(a0)
	
	
	def focusOutEvent(self, a0: QtGui.QFocusEvent) -> None:
		return super().focusOutEvent(a0)
	
	
	
	def onSendMessageTextPress(self):
		#log("press key")
		pass
	
	
	"""
		Событие отправить сообщение
	"""
	def onSendMessageButtonClick(self):
		
		user_name = ""
		if self.connection != None:
			user_name = self.connection.user_name
		
		textEdit: QTextEdit = self.sendMessageText
		message = textEdit.toPlainText()
		
		self.addNewMessage(message, user_name)
		
		textEdit.clear()
		
		# Отправляем всем клиентам сообщение
		#if CHAT_LOCAL:
		if False:
	
			obj = {
				"cmd": "new_message",
				"message": message
			}
			self.sendBroadcastCommand(obj)
		
		else:
			
			for index in range(self.clientList.count()):
				item = self.clientList.item(index)
				client:Client = item.data(1)
				
				obj = {
					"cmd": "new_message",
					"message": message
				}
				self.sendCommand(obj, client.host, client.port)
		
		
	"""
		Добавление нового сообщение в окно чата
	"""
	def addNewMessage(self, message, user_name = ""):
		
		#chatBrowser:QTextBrowser = self.chatBrowser
		chatBrowser:QtWidgets.QPlainTextEdit = self.chatBrowser
		
		time = QTime.currentTime()
		s2 = time.toString("hh:mm:ss")
		
		if user_name != "":
			message = "[{0}] {1}: {2}".format(s2, user_name, message)
		else:
			message = "[{0}] {1}".format(s2, message)
		
		#message = html_escape(message)
		#print(message)
		
		#chatBrowser.append(message)
		chatBrowser.appendPlainText(message)
	
	
	"""
		Поиск клиента по host:port
	"""
	def findClientIndex(self, host:QHostAddress, port:int) -> int:
		
		for index in range(self.clientList.count()):
			item = self.clientList.item(index)
			client:Client = item.data(1)
			
			if client.host == host and client.port == port:
				return index
		
		return -1
	
	
	
	"""
		Удаление старых клиентов
	"""
	def removeOldClients(self):
				
		max_time = int(time.time()) - MAX_CLIENT_TIME
		
		#log ("Max Time = " + str(max_time))
		
		remove_list = []
		for index in range(self.clientList.count(), 0, -1):
			
			index = index - 1
			item = self.clientList.item(index)
			client:Client = item.data(1)
			
			#log ("Client " + client.getClientName() + " " + str(client.time))
			
			if client.time < max_time:
				log ("Remove <" + str(index) + "> " + client.getClientName())
				self.addNewMessage("User " + client.getClientName() + " leave from chat")
				remove_list.append(index)
		
		for index in remove_list:
			self.clientList.takeItem(index)
	
	
	"""
		Обновление клиента, его имени и timestamp метки
		Либо добавление, если клиент не найден
	"""
	def updateClient(self, host:QHostAddress, port:int, user_name: str,
		is_update_time=True, show_message=True):
		
		index = self.findClientIndex(host, port)
		clientList:QtWidgets.QListWidget = self.clientList
		
		if (index == -1):
			client = Client()
			client.user_name = user_name
			client.host = host
			client.port = port
			client.time = int(time.time())
			
			item = QListWidgetItem(client.getClientName())
			item.setData(1, client)
			self.clientList.addItem(item)
			
			if show_message:
				self.addNewMessage("User " + client.getClientName() + " enter to the chat")
		
		else:
			
			item:QListWidgetItem = clientList.item(index)
			client:Client = item.data(1)
			client.user_name = user_name
			if is_update_time:
				client.time = int(time.time())
			
			item.setText( client.getClientName() )
	
	
	"""
		Прием UDP пакетов
	"""
	def processPendingDatagrams(self):
		
		while self.udp_socket.hasPendingDatagrams():
			
			datagram, host, port = self.udp_socket.readDatagram(
					self.udp_socket.pendingDatagramSize() )
			
			client_ip = host.toString()
			#print(client_ip)
			if client_ip[0:4] == "10.5":
			
				try:
					if self.connection:
						msg = str(base64.b64decode( datagram ), ENCODING)
						msg = json.loads(msg)
						
						current_time = int(time.time())
						max_time = current_time + MAX_MESSAGE_TIME
						msg_time = msg["time"]
						
						if max_time > msg_time and self.checkHash(msg, host, port):
							
							cmd = msg["cmd"]
							
							log_message = "Receive '{0}' from {1}:{2}".format(
								cmd, host.toString(), str(port))
							
							try:
							
								if cmd == "ping":
									#log(log_message)
									self.cmdPing(msg, host, port)
								
								elif cmd == "pong":
									#log(log_message)
									self.cmdPong(msg, host, port)
								
								elif cmd == "leave":
									#log(log_message)
									self.cmdLeave(msg, host, port)
								
								elif cmd == "new_message":
									#log(log_message)
									self.cmdNewMessage(msg, host, port)
								
								elif cmd == "get_client_list":
									#log(log_message)
									self.cmdGetClientList(msg, host, port)
								
								elif cmd == "client_list":
									#log(log_message)
									self.cmdClientList(msg, host, port)
							
							except Exception as e:
								log("process pending datagrams Error")
								log(e)
								pass
							
							pass
					
				except Exception as e:
					pass
	
	
	"""
		Проверка хэша UDP пакета
	"""
	def checkHash(self, msg, host:QHostAddress, port:int):
		
		if self.connection == None:
			return False
		
		try:
			message_cmd = msg["cmd"]
			message_time = msg["time"]
			message_user_name = msg["user_name"]
			
			hash_str = "{0}|{1}|{2}|{3}".format(message_cmd, message_time, message_user_name,
				self.connection.secret_key)
			hash1 = msg["hash"]
			hash2 = hashlib.md5( bytes(hash_str, ENCODING) ).hexdigest()
			
			if hash1 == "":
				return False
			
			if hash2 == "":
				return False
			
			if hash1 == hash2:
				return True
			
		except Exception as e:
			pass
		
		return False
		
	
	"""
		Создание хэша UDP пакета
	"""
	def createHash(self, msg):
		
		if self.connection == None:
			return msg
		
		current_time = int(time.time())
		
		hash_str = "{0}|{1}|{2}|{3}".format(msg["cmd"], current_time,
			self.connection.user_name, self.connection.secret_key)
		
		msg["hash"] = hashlib.md5( bytes(hash_str, ENCODING) ).hexdigest()
		msg["user_name"] = self.connection.user_name
		msg["time"] = current_time
		
		return msg
	
	
	
	"""
		Отправка сообщения клиенту host:port
	"""
	def sendCommand(self, obj, host:QHostAddress, port:int):
		
		if self.udp_socket != None:
			obj = self.createHash(obj)
			
			encoding = "utf8"
			msg = json.dumps(obj)
			datagram = base64.b64encode( bytes(msg, encoding) )

			self.udp_socket.writeDatagram(datagram, host, port)
		
		pass
	
	
	"""
		Отправка broadcast сообщения всем клиентам в локальной сети
	"""
	def sendBroadcastCommand(self, obj):
		
		if self.udp_socket != None:
			obj = self.createHash(obj)
			
			encoding = "utf8"
			msg = json.dumps(obj)
			datagram = base64.b64encode( bytes(msg, encoding) )
			"""
			self.udp_socket.writeDatagram(datagram, 
				QHostAddress(QtNetwork.QHostAddress.Broadcast), CHAT_PORT)
			"""
			
			self.udp_socket.writeDatagram(datagram, 
				QHostAddress("10.5.255.255"), CHAT_PORT)
			
		pass
	
	
	"""
		Прием команды ping
	"""
	def cmdPing(self, msg:str, host:QHostAddress, port:int):		
		
		obj = {
			"cmd": "pong",
		}
		
		self.sendCommand(obj, host, port)
		self.updateClient(host, port, msg["user_name"])
	
	
	
	"""
		Прием команды pong
	"""
	def cmdPong(self, msg:str, host:QHostAddress, port:int):
		self.updateClient(host, port, msg["user_name"])
		pass
	
	
	
	"""
		Новое сообщение
	"""
	def cmdNewMessage(self, msg:str, host:QHostAddress, port:int):
		
		self.updateClient(host, port, msg["user_name"])
		
		if (msg["user_name"] != self.connection.user_name):
			self.addNewMessage(msg["message"], msg["user_name"])
		
		self.updateNewMessageTitle()
		
	
	
	"""
		Клиент вышел
	"""
	def cmdLeave(self, msg:str, host:QHostAddress, port:int):
		
		index = self.findClientIndex(host, port)
		
		# Если клиент найден
		if index >= 0:
			item = self.clientList.item(index)
			client:Client = item.data(1)
			
			log ("Remove <" + str(index) + "> " + client.getClientName())
			self.addNewMessage("User " + client.getClientName() + " leave from chat")
			self.clientList.takeItem(index)
	
	
	
	"""
		Отправить команду на получение списка всех клиентов
	"""
	def cmdGetClientList(self, msg:str, host:QHostAddress, port:int):
		
		# Возвращаем список всех клиентов
		
		clients = [];
		
		for index in range(self.clientList.count()):
			item = self.clientList.item(index)
			client:Client = item.data(1)
			
			clients.append(
				{
					"ip": client.host.toString(),
					"port": str(client.port),
					"user_name": client.user_name,
				}
			)
		
		obj = {
			"cmd": "client_list",
			"clients": clients,
		}
		
		self.sendCommand(obj, host, port)
		
		pass
	
	
	
	"""
		Получили список всех клиентов
	"""
	def cmdClientList(self, msg:str, host:QHostAddress, port:int):
		
		# Обновляем список всех клиентов
		try:
			
			clients = msg["clients"]
			
			for item in clients:
				
				try:
					client_ip = QHostAddress(item["ip"])
					client_port = int(item["port"])
					user_name = item["user_name"]
					self.updateClient(client_ip, client_port, user_name, is_update_time=False)
					
				except Exception as e:
					pass	
			
		except Exception as e:
			pass
		
		pass
		
	
	def connectThread(self):
		
		last_broadcast_ping_time = int(time.time())
		last_ping_time = int(time.time())
		last_remove_clients_time = int(time.time())
		last_update_clients_time = int(time.time())
		
		while self.udp_socket != None:
			
			time.sleep(0.1)
			
			current_time = int(time.time())
			
			# Пингуем всех
			try:
				if last_broadcast_ping_time + BROADCAST_PING_TIME_INTERVAL < current_time:
					
					last_broadcast_ping_time = current_time
					
					if CHAT_LOCAL:
						
						#log ("Ping all")
						obj = {
							"cmd": "ping",
						}
						self.sendBroadcastCommand(obj)
					
			except Exception as e:
				log("Ping all error")
				log(e)
					
			
			# Пингуем всех
			try:
				if last_ping_time + PING_TIME_INTERVAL < current_time:
					
					last_ping_time = current_time

					if self.clientList.count() > 0:
						
						#log ("Ping all " + str(self.clientList.count()))
						for index in range(self.clientList.count()):
							item = self.clientList.item(index)
							client:Client = item.data(1)
							
							obj = {
								"cmd": "ping",
							}
							self.sendCommand(obj, client.host, client.port)
					
			except Exception as e:
				log("Ping all error")
				log(e)			
			
			
			# Обновляем список всех клиентов
			try:	
				if last_remove_clients_time + REMOVE_CLIENTS_INTERVAL < current_time:
					
					last_remove_clients_time = current_time
					
					# Получать список клиентов нужно только для не локального чата
					# Для чата в локальной сети достаточно пинга
					if self.clientList.count() > 0:
						
						#log ("Update client list "  + str(self.clientList.count()))
						for index in range(self.clientList.count()):
							item = self.clientList.item(index)
							client:Client = item.data(1)
							
							obj = {
								"cmd": "get_client_list",
							}
							self.sendCommand(obj, client.host, client.port)
				
			except Exception as e:
				log("Update client error")
				log(e)
			
			
			
			# Удаляем устаревших клиентов
			try:
				if last_update_clients_time + UPDATE_CLIENTS_INTERVAL < current_time:
					
					last_update_clients_time = current_time
					
					if self.clientList.count() > 0:
						#log ("Remove old clients")
						self.removeOldClients()
			
			except Exception as e:
				pass
			
			
			pass
		
		log ("Leave from thread")
		
	
		
	
	def disconnectFromChat(self):
		
		main_helper.stop_peervpn()
		
		if self.udp_socket != None:
			
			# Отправляем всем клиентам уведомление о том что вышли из чата
			if self.clientList.count() > 0:
						
				for index in range(self.clientList.count()):
					item = self.clientList.item(index)
					client:Client = item.data(1)
					
					obj = {
						"cmd": "leave",
					}
					self.sendCommand(obj, client.host, client.port)
			
			# Отключаем сокет
			self.udp_socket.disconnectFromHost()
			self.udp_socket.disconnect()
			self.udp_socket = None
			log ("Disconnected from chat " + self.connection.connection_name)
			self.addNewMessage("Disconnected from chat " + self.connection.connection_name)
			
		self.connection = None
		self.is_connected = False
		
		# Clear clients
		self.clientList.clear()
	
	
	
	def connectToChat(self, connection:Connection):
		
		if self.udp_socket != None:
			self.disconnectFromChat()
			time.sleep(0.5)
		
		# Setup connection
		self.connection = connection
		
		self.addNewMessage("Connect to " + self.connection.connection_name)
		self.addNewMessage("Known clients: " + self.connection.connection_string)
		log ("Connect to chat " + self.connection.connection_name)
		
		self.addNewMessage("Your Local IP: " + self.connection.local_ip)
		
		# Run peervpn
		main_helper.run_peervpn(self.connection)
		
		#time.sleep(1)
		
		# Open udp socket
		self.udp_socket = QUdpSocket(self)
		if CHAT_LOCAL:
			self.udp_socket.bind(QHostAddress("0.0.0.0"), CHAT_PORT)
		else:
			self.udp_socket.bind(QHostAddress("0.0.0.0"), self.connection.client_port)
		self.udp_socket.readyRead.connect(self.processPendingDatagrams)
		
		# Connect thread
		self.thread_connect = threading.Thread(target=self.connectThread)
		self.thread_connect.daemon = True
		self.thread_connect.start()
		
		# Connect to clients
		connection:Connection = self.connection
		
		# Send ping message to clients
		if CHAT_LOCAL:
			
			obj = {
				"cmd": "ping",
			}
			self.sendBroadcastCommand(obj)
			
		else:
			client_list = connection.getConnectionList()
			for client in client_list:
				
				client_ip:QHostAddress = client[0]
				client_port:int = client[1]
				
				connect_title = "Connect to {0}:{1}".format(client_ip.toString(), str(client_port))
				log (connect_title)
				
				self.updateClient(client_ip, client_port, "?", 
					is_update_time=False, show_message=False)
				
				obj = {
					"cmd": "ping",
				}
				self.sendCommand(obj, client_ip, client_port)
				
				obj = {
					"cmd": "get_client_list",
				}
				self.sendCommand(obj, client_ip, client_port)
			
		pass
		



def run():
	
	# Create app
	app = QApplication(sys.argv)
	main_window = MainWindow()
	main_helper.main_window = main_window
	
	log("Initialization")
	
	# Find peervpn
	main_helper.find_peervpn()
	log ("PeerVPN path = " + main_helper.peer_vpn_dir_path)
	
	# Start stdout thread
	main_helper.start_process_stdout_thread()
	
	log("Start")
	
	# Start app
	main_window.show()
	app_result = app.exec()
	
	main_helper.is_terminated = True
	sys.exit(app_result)