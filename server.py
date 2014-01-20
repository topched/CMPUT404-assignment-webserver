import SocketServer, os, time
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Kris Kushniruk
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
	def handle(self):

		self.data = self.request.recv(1024).strip()

		#print self.client_address
		
		self.header=""
		self.body=""

		self.parse_request()
		self.request.sendall(self.header + "\n")
		self.request.sendall(self.body)		

	def parse_request(self):

		request = self.data.split()

		if len(request) > 0:
			command = request[0]
			path = request[1]
			version = request[2]
		else:
			return

		#Only want get commands
		if command != "GET":
			return
			 
		#Only want to serve HTTP/1.1
		if version != "HTTP/1.1":
			return

		if path == "/":
			path = "/index.html"
		elif path.endswith("/"):
			path += "index.html"

		self.open_path(path)
					

	def open_path(self, path):
			
		fileName = os.getcwd() + "/www" + path

		try:
			f=open(fileName, "r")
			ft = self.file_type(fileName)
			if ft == "error":
				raise IOError
			self.header += "HTTP/1.1 200 OK\n"
			self.header += ft
			self.header += "Content-length: %d\n" % os.path.getsize(fileName)
			self.header += "Date: %s\n" % self.date_time()
			self.body += f.read()
			f.close()
		except (IOError, OSError):
			self.header += "HTTP/1.1 404\n"
			self.body += "Page Not Found\n"
	
	def file_type(self, path):
		
		if path.endswith(".html"):
			return "Content-type: text/html\n"		
		elif path.endswith(".css"):
			return "Content-type: text/css\n"
		else:
			return "error"

	def date_time(self):

		weekdayname = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
		monthname = [None,'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

		now = time.time()
		year, month, day, hh, mm, ss, wd, y, z = time.localtime(now)
		s = "%s, %02d %3s %4d %02d:%02d:%02d GMT" % (weekdayname[wd],day,monthname[month],year,hh,mm,ss)
		return s


		

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    ip, port = server.serve_forever()
