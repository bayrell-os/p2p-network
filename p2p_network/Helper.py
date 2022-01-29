# -*- coding: utf-8 -*-

import sys, threading, time, base64, json, hashlib, os, io, subprocess

from .Connect import Connection
from PyQt5.QtCore import QTime, QDate


class Helper:
	
	def format_log_date(self, msg):
		date = QDate.currentDate()
		time = QTime.currentTime()
		s1 = date.toString("yyyy-MM-dd")
		s2 = time.toString("hh:mm:ss")
		return "[{0} {1}] {2}".format(s1, s2, msg)
	
	
	def peervpn_log(self, msg, format=False):
		
		if not self.is_terminated:
			
			if format:
				msg = self.format_log_date(msg) + "\n"
			
			if self.enable_logs:
				main_window = self.main_window
				if main_window != None:
					if main_window.peervpnLogWindow != None:
						main_window.peervpnLogWindow.logText.insertPlainText(msg)
	
	
	def app_log(self, msg):
		if not self.is_terminated:
			msg = self.format_log_date(msg)
			
			print (msg)
			
			if self.enable_logs:
				main_window = self.main_window
				if main_window != None:
					if main_window.appLogWindow != None:			
						main_window.appLogWindow.logText.appendPlainText(msg)
	
	
	def __init__(self):
		self.peer_vpn_dir_path = ""

		self.peervpn_thread = None
		self.peervpn_proc = None
		self.main_window = None
		self.is_terminated = False
		self.enable_logs = False
		
		#self.first, self.second = pty.openpty()
		if sys.platform[0:5] == "linux" and self.enable_logs:
			self.first, self.second = os.openpty()


	def get_peervpn_config(self):
		path = os.path.expanduser('~')
		path = os.path.join(path, ".config", "p2p_chat")
		os.makedirs(path, exist_ok=True)
		file_name = os.path.join(path, "peervpn.config")
		return file_name


	"""
		Функция, которая отслеживает stdout запущенного процесса
	"""
	def process_stdout(self, stdout:io.TextIOWrapper):
		while True:		
			out = stdout.read(5)	
			self.peervpn_log(out)

	"""
		Запуск потока stdout
	"""
	def start_process_stdout_thread(self):
		
		if sys.platform[0:5] == "linux" and self.enable_logs:
			stdout = io.open(self.first, 'r', encoding='UTF-8', newline='\n')
			p1 = threading.Thread(target=self.process_stdout, args=(stdout,))
			p1.daemon = True
			p1.start()
	

	"""
		Поиск программы peervpn
	"""
	def find_peervpn(self):
		search_dir = os.path.realpath(__file__)
		
		for i in range(10):
			peervpn_dir = os.path.join(search_dir, "peervpn")
			if os.path.exists(peervpn_dir):
				self.peer_vpn_dir_path = peervpn_dir
				break
			search_dir = os.path.dirname(search_dir)

	
	"""
		Запуск программы peervpn
	"""
	def start_peervpn(self, connection:Connection):
		
		try:
			peervpn_config = self.get_peervpn_config()
			
			# Get vpn version
			peervpn_bin = "peervpn.64bit.exe"
			
			if connection.vpn_version == "32bit":
				peervpn_bin = "peervpn.32bit.exe"
				
			if sys.platform[0:5] == "linux":
				peervpn_bin = "peervpn.ubuntu.18.04"
				
			cmd = os.path.join(self.peer_vpn_dir_path, 'bin', peervpn_bin)
			
			if sys.platform[0:5] == "linux" and self.enable_logs:
				self.peervpn_proc = subprocess.Popen(
					[cmd, peervpn_config],
					stdout=self.second, 
					stderr=self.second, 
					close_fds=True, 
					bufsize=0
				)
			
			else:
				self.peervpn_proc = subprocess.Popen(
					[cmd, peervpn_config],
					close_fds=True, 
					bufsize=0
				)
			
			self.app_log( "Start PeerVPN PID=" + str(self.peervpn_proc.pid) )
			#self.peervpn_log("Start PeerVPN PID=" + str(self.peervpn_proc.pid), format=True)
			
			output_result = 1
			while output_result != 0 and not self.is_terminated and self.peervpn_proc != None:
				output_result = self.peervpn_proc.poll()
				if (output_result == 0):
					break
				time.sleep(0.1)
			
		except Exception as e:
			self.app_log("PeerVPN Error")
			self.app_log(e)
			pass
			
		self.peervpn_thread = None
		
	
	def stop_app_by_pid(self, pid):
		try:
			os.kill(pid, 9)
		
		except Exception as e:
			pass
	
			
	def stop_peervpn(self):
		if self.peervpn_proc != None:
			self.peervpn_log("Stop PeerVPN pid=" + str(self.peervpn_proc.pid), format=True)
			self.app_log("Stop PeerVPN pid=" + str(self.peervpn_proc.pid))
			self.stop_app_by_pid(self.peervpn_proc.pid)
			self.peervpn_proc = None
	
	
	def create_peervpn_config(self, connection:Connection):
		peervpn_config = self.get_peervpn_config()
		content = ""
		
		initpeers = ""
		list = connection.getConnectionList()
		for item in list:
			initpeers += item[0].toString() + " " + str(item[1]) + " "
		
		content += "ifconfig4 " + connection.local_ip + "/16" + "\n"
		content += "initpeers " + initpeers + "\n"
		content += "networkname " + connection.connection_name + "\n"
		content += "psk " + connection.secret_key + "\n"

		content += "interface peervpn0" + "\n"
		content += "port " + str(connection.client_port) + "\n"
		content += "enableipv4 yes" + "\n"
		content += "enableipv6 no" + "\n"
		content += "enabletunneling yes" + "\n"
		
		if connection.enable_relay:
			content += "enablerelay yes" + "\n"
		else:
			content += "enablerelay no" + "\n"
		
		if sys.platform[0:5] == "linux":
			content += "user peervpn" + "\n"
			content += "group peervpn" + "\n"
			content += "chroot /tmp" + "\n"
		
		with open(peervpn_config, "w") as file:
			file.write(content)
			file.close()
	
	
	"""
		Запуск peervpn
	"""
	def run_peervpn(self, connection:Connection):
		
		peervpn_config = self.get_peervpn_config()
		
		self.create_peervpn_config(connection)
		
		self.app_log( "PeerVPN config = " + peervpn_config )
		
		if connection.auto_start_vpn:
			self.peervpn_thread = threading.Thread(target=self.start_peervpn, args=(connection,))
			self.peervpn_thread.daemon = True
			self.peervpn_thread.start()
			
		else:
			self.app_log( "PeerVPN autostart is disabled. Start manual bat file" )
