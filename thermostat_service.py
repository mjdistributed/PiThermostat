import serial
import glob
import subprocess
import urllib
import SimpleHTTPServer
import SocketServer
import os
import cgi
import socket

from BaseHTTPServer import HTTPServer
from Thermostat import Thermostat

def set_phase(phase, thermostat):
	""" Sets thermostat either 'ON' or 'OFF' depending on phase """
	phase = phase.upper()
	if (phase == "ON"):
		thermostat.turn_on()
	elif (phase == "OFF"):
		thermostat.turn_off()
	else:
		raise ValueError("Bad phase: '" + phase + "', should be 'ON' or 'OFF'")
 
#Create custom HTTPRequestHandler class
class CustomHTTPRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
  
	# trying to be fancy w/ OO (not working)
	#def __init__(self, request, client_address, server):
	#	super(CustomHTTPRequestHandler, self).__init__(request, client_address, server)
	#	self.thermostat = Thermostat()		


	thermostat = Thermostat()

	#handle GET command
	def do_GET(self):
		print("doing get...")
		print("path: " + str(self.path))
		try:
			html = ""
			if "." in self.path and not '?' in self.path:
				print("loading static file: " + self.path)
				# load static files as needed
				f = open("." + self.path)
				html = f.read()
				f.close()
			else:
				# generate dynamic html result
				if ('?phase=' in self.path):
					phase = self.path[self.path.index('=') + 1:]
					set_phase(phase, self.thermostat)
				if ('?' in self.path):
					self.path = self.path[:self.path.index('?')]
				#### construct returned html
				# add buttons for running programs

			#send code 200 response
			self.send_response(200)

			#send header first
			self.send_header('Content-type','text-html')
			self.end_headers()

			#send file content to client
			html = "<p> Hello World! </p>"
			self.wfile.write(html)
			print("done doing get...")
			return

		except IOError:
		  self.send_error(404, 'file not found')

class HTTPServerV6(HTTPServer):
  address_family = socket.AF_INET6
	  
def run():
  	print('http server is starting...')
  	#ip and port of server <- IP set dynamically
  	server_address = ('', 8072)
  	httpd = HTTPServerV6(server_address, CustomHTTPRequestHandler)
  	# httpd = SocketServer.TCPServer(server_address, CustomHTTPRequestHandler)
  	print('http server is running...')
	try:
  		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	print("closing server")
	httpd.server_close()
  
if __name__ == '__main__':
  run()
