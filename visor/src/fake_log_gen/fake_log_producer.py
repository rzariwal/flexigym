from src.fake_log_gen import fake_log_gen
import kafka
from kafka import KafkaProducer
from kafka.errors import KafkaError

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

# Used to generate Apache Access Logs
# And send to Kafka
class fake_access_producer(fake_log_gen.fake_access_gen):

	def run(self):
		self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
		super(fake_access_producer, self).run()

	@coroutine
	def heartbeat_lines(self):
		while True:
			t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')	
			data = '- - - [%s] "%s" - -' % (t, self.config["heartbeat"]["message"])
			self.log.info(data)
			#self.client.send((data+'\n').encode())	
			self.producer.send(self.topic, (data+'\n').encode())	
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
			#self.client.send((data+'\n').encode())
			self.producer.send(self.topic, (data+'\n').encode())
			yield from asyncio.sleep(random.uniform(self.access_min, self.access_max))
	

# Used to generate Apache Error Logs
# And send to Kafka
class fake_error_producer(fake_log_gen.fake_error_gen):

	def run(self):
		self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
		super(fake_error_producer, self).run()
    
	@coroutine
	def heartbeat_lines(self):
		while True:
			data = "[-] [-] " + self.config["heartbeat"]["message"]
			self.log.info(data)	
			self.producer.send(self.topic, (data+'\n').encode())
			yield from asyncio.sleep(int(self.config["heartbeat"]["interval"]))

	@coroutine
	def info_lines(self):
		while True:
			pid = ''.join(str(random.randint(0, 9)) for i in range(5))
			tid = ''.join(str(random.randint(0, 9)) for i in range(10))
			# Select ip from the initilized ip pool of size self.ip_num
			# Apply a binomial distribution (discrete normal dist)
			# to select ips from the pool
			ip_index = numpy.random.binomial(n=self.ip_num, p=0.8, size=1)
			ip = self.ips[ip_index]
			
			# "%a %b %d %H:%M:%S %Y"
			now = time.localtime()
			asctime = '[' + time.strftime("%a %b %d %H:%M:%S %Y", now) + '] '
			level_name = '[INFO] '
			msg = "[pid %s:tid %s] [client %s] %s" % (pid, tid, ip, self.infos[random.randrange(len(self.infos))])
			data = asctime + level_name + msg
			self.log.info(data)
			self.producer.send(self.topic, (data+'\n').encode())
			
			if not self.info_peak_flag:
				info_normal = self.info_normal[random.randint(0, len(self.info_normal)-1)]
				yield from asyncio.sleep(random.uniform(info_normal[0], info_normal[1]))
				if self.info_peak_counter > 50:
					self.info_peak_flag = True
					self.info_peak_counter = 0
				else:
					self.info_peak_counter += random.uniform(0.05,0.5)
			else:
				info_peak = self.info_peak[random.randint(0, len(self.info_peak)-1)]
				yield from asyncio.sleep(random.uniform(info_peak[0], info_peak[1]))	
				if self.info_peak_counter > 350:
					self.info_peak_flag = False
					self.info_peak_counter = 0
				else:
					self.info_peak_counter += random.uniform(1, 1.2)


	@coroutine
	def warn_lines(self):
		while True:
			pid = ''.join(str(random.randint(0, 9)) for i in range(5))
			tid = ''.join(str(random.randint(0, 9)) for i in range(10))
			# Select ip from the initilized ip pool of size self.ip_num
			# Apply a binomial distribution (discrete normal dist)
			# to select ips from the pool
			ip_index = numpy.random.binomial(n=self.ip_num, p=0.8, size=1)
			ip = self.ips[ip_index]
			# "%a %b %d %H:%M:%S %Y"
			now = time.localtime()
			asctime = '[' + time.strftime("%a %b %d %H:%M:%S %Y", now) + '] '
			level_name = '[WARNING] '
			msg = "[pid %s:tid %s] [client %s] %s" % (pid, tid, ip, self.warnings[random.randrange(len(self.warnings))])
			data = asctime + level_name + msg
			self.log.warning(data)
			#self.client.send((data+'\n').encode())
			self.producer.send(self.topic, (data+'\n').encode())

			# Peak gerenation control
			if not self.warn_peak_flag:
				warn_normal = self.warn_normal[random.randint(0, len(self.warn_normal)-1)]
				yield from asyncio.sleep(random.uniform(warn_normal[0], warn_normal[1]))
				if self.warn_peak_counter > 50:
					self.warn_peak_flag = True
					self.warn_peak_counter = 0
				else:
					self.warn_peak_counter += random.uniform(0.05,0.5)
			else:
				warn_peak = self.warn_peak[random.randint(0, len(self.warn_peak)-1)]
				yield from asyncio.sleep(random.uniform(warn_peak[0], warn_peak[1]))
				if self.warn_peak_counter > 250:
					self.warn_peak_flag = False
					self.warn_peak_counter = 0
				else:
					self.warn_peak_counter += random.uniform(1, 1.2)


	@coroutine
	def error_lines(self):
		while True:
			pid = ''.join(str(random.randint(0, 9)) for i in range(5))
			tid = ''.join(str(random.randint(0, 9)) for i in range(10))
			# Select ip from the initilized ip pool of size self.ip_num
			# Apply a binomial distribution (discrete normal dist)
			# to select ips from the pool
			ip_index = numpy.random.binomial(n=self.ip_num, p=0.8, size=1)
			ip = self.ips[ip_index]
	
			now = time.localtime()
			asctime = '[' + time.strftime("%a %b %d %H:%M:%S %Y", now) + '] '
			level_name = '[ERROR] '
			msg = "[pid %s:tid %s] [client %s] %s" % (pid, tid, ip, self.errors[random.randrange(len(self.errors))])
			data = asctime + level_name + msg
			self.log.error(data)
			#self.client.send((data+'\n').encode())
			self.producer.send(self.topic, (data+'\n').encode())

			# Peak gerenation control
			if not self.error_peak_flag:
				error_normal = self.error_normal[random.randint(0, len(self.error_normal)-1)]
				yield from asyncio.sleep(random.uniform(error_normal[0], error_normal[1]))
				if self.error_peak_counter > 20:
					self.error_peak_flag = True
					self.error_peak_counter = 0
				else:
					self.error_peak_counter += random.uniform(0.2,0.5)
			else:
				error_peak = self.error_peak[random.randint(0, len(self.error_peak)-1)]
				yield from asyncio.sleep(random.uniform(error_peak[0], error_peak[1]))	
				if self.error_peak_counter > 150:
					self.error_peak_flag = False
					self.error_peak_counter = 0
				else:
					self.error_peak_counter += random.uniform(1, 1.2)		


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

	# Load the kafka topic
	with open(os.environ['VISORHOME']+"/config/kafka_monitor.json") as kafka_config_file:
		kafka_config = json.load(kafka_config_file)

	# Instantiate a fake log generator
	if mode == 'access':
		log_producer = fake_access_producer(log, config, kafka_config, mode)
	else:
		log_producer = fake_error_producer(log, config, kafka_config, mode)

	log_producer.run()


if __name__ == "__main__":
	main()

	


