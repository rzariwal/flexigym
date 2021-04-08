# Fake log files generator

import os
import random
import json
import logging
import argparse
import asyncio
import datetime
from asyncio import coroutine
import numpy
import pytz


class fake_log_gen(object):

    def __init__(self, log, config, kafka_config, mode):
        self.log = log
        self.mode = mode
        # Dict that contains config info
        self.config = config
        self.topic = kafka_config["kafka"]["topic"]

    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(
            asyncio.wait([
                self.heartbeat_lines()]
            )
        )
        loop.close()


#############################
# Apache Access Log Generator
#############################
class fake_access_gen(fake_log_gen):

    def __init__(self, log, config, kafka_config, mode):
        self.log = log
        self.mode = mode
        # Dict that contains config info
        self.config = config
        self.root_url = config["access"]["root_url"]
        self.access_min = self.config["access"]["interval"]["min"]
        self.access_max = self.config["access"]["interval"]["max"]
        self.user_ids = self.config["access"]["user_id"]
        self.methods = self.config["access"]["method"]
        self.methods_dist = self.config["access"]["method_dist"]
        self.resources = self.config["access"]["resource"]
        self.codes = self.config["access"]["code"]
        self.codes_dist = self.config["access"]["code_dist"]
        self.versions = self.config["access"]["version"]
        self.device = self.config["access"]["device"]
        self.browser = config["access"]["browser"]
        self.geolocation = config["access"]["geolocation"]
        self.tenant_id = config["access"]["tenant_id"]
        self.timezone = config["access"]["timezone"]
        self.country = config["access"]["country"]
        self.screenResolution = config["access"]["screenResolution"]
        self.action = config["access"]["action"]
        self.timeOnPage = config["access"]["timeOnPage"]
        self.supplier_id = config["access"]["supplier_id"]
        self.topic = kafka_config["kafka"]["topic"]


    def run(self):
        self.loop = asyncio.get_event_loop()
        try:
            self.loop.run_until_complete(
                asyncio.wait([
                    self.heartbeat_lines(),
                    self.access_lines()]
                    # self.heartbeat_lines()]
                )
            )
        finally:
            self.loop.close()

    @coroutine
    def heartbeat_lines(self):
        while True:
            # for i in range(3):
            tms = int(datetime.datetime.now(tz=pytz.utc).timestamp() * 1000)
            t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')
            self.log.info('- - - [%s] "%s" [%s]- -', t, self.config["heartbeat"]["message"], tms)
            yield from asyncio.sleep(int(self.config["heartbeat"]["interval"]))

    @coroutine
    def access_lines(self):
        """
        Log looks something like this
        { "ip": xxx.xxx.xxx.xxx, "device": "Laptop", "browser": "Safari", "c":"SG", "r":"FlexiGym", "u":"url",
        "t": "in ms", "ll": [ 19.434200, -99.138603 ], "tz":"SST", "user_id":50, "tenant_id":1,
        "screenResolution":"1440 x 900", "action":"subscribe", "timeOnPage":5 }
        """
        while True:
            ip = '.'.join(str(random.randint(0, 255)) for i in range(4))
            user_identifier = '-'
            user_id = self.user_ids[random.randint(0, len(self.user_ids) - 1)]
            tms = int(datetime.datetime.now(tz=pytz.utc).timestamp() * 1000)
            t = datetime.datetime.now().strftime('%d/%b/%Y:%H:%M:%S -0700')
            device = self.device[random.randint(0, len(self.device) - 1)]
            method = numpy.random.choice(self.methods, p=self.methods_dist)
            resource = self.resources[random.randint(0, len(self.resources) - 1)]
            version = self.versions[random.randint(0, len(self.versions) - 1)]
            msg = method + " " + self.root_url + resource + " " + version
            code = numpy.random.choice(self.codes, p=self.codes_dist)
            size = random.randint(1024, 10240)
            self.log.info('%s %s %s [%s] "%s" %s %s %s', ip, user_identifier, user_id, t, tms, msg, code, size)
            yield from asyncio.sleep(random.uniform(self.access_min, self.access_max))


#############################
#  Apache Error Log Generator
#############################
class fake_error_gen(fake_log_gen):

    def __init__(self, log, config, kafka_config, mode):
        self.log = log
        self.mode = mode
        # Dict that contains config info
        self.config = config

        # Config for [INFO] logs
        self.info_normal = self.config["info"]["interval"]["normal"]
        self.info_peak = self.config["info"]["interval"]["peak"]
        self.infos = self.config["info"]["message"]

        self.info_peak_flag = False
        self.info_peak_counter = 0

        # Config for [WARN] logs
        self.warn_normal = self.config["warn"]["interval"]["normal"]
        self.warn_peak = self.config["warn"]["interval"]["peak"]
        self.warnings = self.config["warn"]["message"]

        self.warn_peak_flag = False
        self.warn_peak_counter = 0

        # Config for [ERROR] logs
        self.error_normal = self.config["error"]["interval"]["normal"]
        self.error_peak = self.config["error"]["interval"]["peak"]
        self.errors = self.config["error"]["message"]

        self.error_peak_flag = False
        self.error_peak_counter = 0

        # Config for Kafka topic to produce into
        self.topic = kafka_config["kafka"]["topic"]

        # ip (client address) pool generation
        # with the pool size of 50
        self.ip_num = 50
        self.ips = ['.'.join(str(random.randint(0, 255)) for i in range(4)) for i in range(self.ip_num)]

    def run(self):
        loop = asyncio.get_event_loop()
        # The event loop
        loop.run_until_complete(
            asyncio.wait([
                self.heartbeat_lines(),
                self.info_lines(),
                self.warn_lines(),
                self.error_lines()]
            )
        )
        loop.close()

    @coroutine
    def heartbeat_lines(self):
        while True:
            self.log.info("[-] [-] " + self.config["heartbeat"]["message"])
            yield from asyncio.sleep(int(self.config["heartbeat"]["interval"]))

    @coroutine
    def access_lines(self):
        while True:
            ip = '.'.join(str(random.randint(0, 255)) for i in range(4))
            # user_identifier =
            # user_id =
            self.log.info("%s", ip)
            yield from asyncio.sleep(random.uniform(self.access_min, self.access_max))

    @coroutine
    def warn_lines(self):
        while True:
            pid = ''.join(str(random.randint(0, 9)) for i in range(5))
            tid = ''.join(str(random.randint(0, 9)) for i in range(10))
            ip = '.'.join(str(random.randint(0, 255)) for i in range(4))
            self.log.warning("[pid %s:tid %s] [client %s] %s", pid, tid, ip,
                             self.warnings[random.randrange(len(self.warnings))])
            yield from asyncio.sleep(random.uniform(self.warn_min, self.warn_max))

    @coroutine
    def error_lines(self):
        while True:
            pid = ''.join(str(random.randint(0, 9)) for i in range(5))
            tid = ''.join(str(random.randint(0, 9)) for i in range(10))
            ip = '.'.join(str(random.randint(0, 255)) for i in range(4))
            self.log.error("[pid %s:tid %s] [client %s] %s", pid, tid, ip,
                           self.errors[random.randrange(len(self.errors))])
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
        log_format = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", "%a %b %d %H:%M:%S %Y")
    else:
        log_format = logging.Formatter("%(message)s")
    # Set the Formatter for this Handler to form
    out.setFormatter(log_format)
    # Add the file Handler 'out' to the logger'log'
    log.addHandler(out)

    # Test Logging
    '''log.info("INFO!")
    log.error("Error!")
    '''

    # Load the configure json file to a dict
    # with open(os.environ['VISORHOME']+"/config/fake_log_gen.json") as config_file:
    # 	config = json.load(config_file)
    #
    # # Load the configure json file to a dict
    # with open(os.environ['VISORHOME']+"/config/kafka_monitor.json") as config_file:
    # 	kafka_config = json.load(config_file)

    with open("D:\\flexigym\\visor\\config\\fake_log_gen.json") as config_file:
        config = json.load(config_file)

    # Load the configure json file to a dict
    with open("D:\\flexigym\\visor\\config\\kafka_monitor.json") as config_file:
        kafka_config = json.load(config_file)

    # Instantiate a fake log generator
    if mode == 'error':
        log_gen = fake_error_gen(log, config, kafka_config, mode)
    else:
        log_gen = fake_access_gen(log, config, kafka_config, mode)
    log_gen.run()


if __name__ == "__main__":
    main()
