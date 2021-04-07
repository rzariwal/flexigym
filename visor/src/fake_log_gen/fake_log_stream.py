from src.fake_log_gen import fake_log_gen
import socket

import os
import random
import json
import logging
import argparse
import asyncio
import datetime
import time
from asyncio import coroutine
import numpy


class fake_access_stream(fake_log_gen.fake_access_gen):

	def run(self):
		#super(fake_access_stream, self).__init__(log, config, mode)
		# Create a TCP/IP socket object
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# Get local machine name
		host = socket.gethostbyname(socket.gethostname())
		print('>>> Host Name:\t%s' % str(host))
		# Reserve a hst for your service
		port = 5555
		server_addr = (host, port)
		# Bind the socket with the server address
		self.s.bind(server_addr)
		print('>>> Listening on port:\t%s' % str(port))
		# Calling listen() puts the socket into server mode
		self.s.listen(5)
		print('>>> Waiting for client connection')
		# accept() waits for an incoming connection
		# Establish connection with client
		self.client, self.addr = self.s.accept()
		print('>>> Received request from ' + str(self.addr))

		super(fake_access_stream, self).run()

	@coroutine
	def heartbeat_lines(self):
		while True:
			t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')	
			data = '- - - [%s] "%s" - -' % (t, self.config["heartbeat"]["message"])
			self.log.info(data)
			self.client.send((data+'\n').encode())	
				
			yield from asyncio.sleep(int(self.config["heartbeat"]["interval"]))

	@coroutine
	def access_lines(self):
		while True:
			ip = '.'.join(str(random.randint(0, 255)) for i in range(4))
			user_identifier = '-'
			user_id = self.user_ids[random.randint(0,len(self.user_ids)-1)]
			t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')

			method = numpy.random.choice(self.methods, p=self.methods_dist)
			resource = self.resources[random.randint(0, len(self.resources)-1)]
			version = self.versions[random.randint(0, len(self.versions)-1)]
			msg = method + " " + resource + " " + version
			code = numpy.random.choice(self.codes, p=self.codes_dist)
			size = random.randint(1024, 10240)
			data = '%s %s %s [%s] "%s" %s %s' % (ip, user_identifier, user_id, t, msg, code, size)
			self.log.info(data)
			self.client.send((data+'\n').encode())
			yield from asyncio.sleep(random.uniform(self.access_min, self.access_max))
	

class fake_error_stream(fake_log_gen.fake_error_gen):

	def run(self):
		#super(fake_error_stream, self).__init__(log, config, mode)
		# Create a TCP/IP socket object
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		# Get local machine name
		host = socket.gethostbyname(socket.gethostname())
		print('>>> Server Host Name:\t%s' % str(host))
		# Reserve a hst for your service
		port = 5555
		server_addr = (host, port)
		# Bind the socket with the server address
		self.s.bind(server_addr)
		print('>>> Server is listening on port:\t%s' % str(port))
		# Calling listen() puts the socket into server mode
		self.s.listen(5)
		print('>>> Server is waiting for client connection')
		# accept() waits for an incoming connection
		# Establish connection with client
		self.client, self.addr = self.s.accept()
		print('>>> Server received request from ' + str(self.addr))

		super(fake_error_stream, self).run()
    
	@coroutine
	def heartbeat_lines(self):
		while True:
			data = "[-] [-] " + self.config["heartbeat"]["message"]
			self.log.info(data)
			self.client.send((data+'\n').encode())
			yield from asyncio.sleep(int(self.config["heartbeat"]["interval"]))

	@coroutine
	def warn_lines(self):
		while True:
			pid = ''.join(str(random.randint(0, 9)) for i in range(5))
			tid = ''.join(str(random.randint(0, 9)) for i in range(10))
			ip = '.'.join(str(random.randint(0, 255)) for i in range(4))
			# "%a %b %d %H:%M:%S %Y"
			now = time.localtime()
			asctime = '[' + time.strftime("%a %b %d %H:%M:%S %Y", now) + '] '
			level_name = '[ERROR] '
			msg = "[pid %s:tid %s] [client %s] %s" % (pid, tid, ip, self.warnings[random.randrange(len(self.warnings))])
			data = asctime + level_name + msg
			self.log.warning(data)
			self.client.send((data+'\n').encode())
			yield from asyncio.sleep(random.uniform(self.warn_min, self.warn_max))

	@coroutine
	def error_lines(self):
		while True:
			pid = ''.join(str(random.randint(0, 9)) for i in range(5))
			tid = ''.join(str(random.randint(0, 9)) for i in range(10))
			ip = '.'.join(str(random.randint(0, 255)) for i in range(4))
			now = time.localtime()
			asctime = '[' + time.strftime("%a %b %d %H:%M:%S %Y", now) + '] '
			level_name = '[WARNING] '
			msg = "[pid %s:tid %s] [client %s] %s" % (pid, tid, ip, self.errors[random.randrange(len(self.errors))])
			data = asctime + level_name + msg
			self.log.error(data)
			self.client.send((data+'\n').encode())
			yield from asyncio.sleep(random.uniform(self.error_min, self.error_max))

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-o", help="fake logfile")
	parser.add_argument("-m", help="log mode")
	args = parser.parse_args()

	# Identify the log format
	mode = args.m
	if mode not in ['error', 'access']:
		print('Argument error.')

	# Instantiate the logger
	log = logging.getLogger('Gen')
	# Set the level
	logging.basicConfig(level=logging.INFO)
	# Instantiate a file Handler
	out = logging.FileHandler(args.o)
	# Instantiate a Formatter
	# Format the time string
	if mode == 'error':
		#log_format = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%a %b %d %H:%M:%S %Y")
		log_format = logging.Formatter("%(message)s")
	else:
		log_format = logging.Formatter("%(message)s")
	# Set the Formatter for this Handler to form
	out.setFormatter(log_format)
	# Add the file Handler 'out' to the logger'log'
	log.addHandler(out)

	# Load the configure json file to a dict
	with open(os.environ['VISORHOME']+"/config/fake_log_gen.json") as config_file:
		config = json.load(config_file)

	# Instantiate a fake log generator
	if mode == 'access':
		log_streamer = fake_access_stream(log, config, mode)
	else:
		log_streamer = fake_error_stream(log, config, mode)

	log_streamer.run()


if __name__ == "__main__":
	main()




 
