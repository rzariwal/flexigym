from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql import SparkSession,SQLContext
from pyspark.sql.types import StructType,StructField,DoubleType,StringType
from datetime import datetime
import json
import happybase
import os
import smtplib
import time
import os
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 pyspark-shell'

class kafka_monitor(object):

    def __init__(self, config, config_private):
        # Load config file
        self.config = config
        # Load private config file
        self.config_private = config_private
        # Set the Kafka related params
        self.addr = self.config['kafka']['addr']
        self.topic = self.config['kafka']['topic']

        # Set the summary report params
        # report interval: in terms of sec
        self.report_interval = self.config['email']['report']['interval']
        # The batch interval may also be used aside the sparkstreamingcontext creation
        self.batch_interval = self.config['batch_interval']

        # Count the total number of logs
        # Used in summary report system
        self.total_log_num = 0

        # Pick out the top ips in all logs
        self.top_ips=[('None', 0) for i in range(3)]
        # Pick out the top ips in [ERROR] logs
        self.top_error_ips=[('None', 0) for i in range(3)]


    def functionToCreateContext(self):
        # Define Spark configuration
        conf = SparkConf()
        conf.setMaster(self.config['master_url'])
        conf.setAppName(self.config['app_name'])
        #conf.set("spark.cores.max", "2")
        conf.set("spark.streaming.backpressure.enabled",True)
        #conf.set("spark.streaming.backpressure.initialRate", "60")
        # Can set the max rate per kafka partition if needed
        conf.set("spark.streaming.kafka.maxRatePerPartition", "100")
        # Initialize a SparkContext
        sc = SparkContext(conf=conf)
        spark = SparkSession(sc)
        # Set the batch interval to be 1 sec
        ssc = StreamingContext(sc, self.config['batch_interval'])
        def savetohdfs(rdd):
            if not rdd.isEmpty():
                schema = StructType([StructField("IP", StringType(), True),
                                     StructField("user_identifier", StringType(), True),
                                     StructField("user_id", StringType(), True),
                                     StructField("user_name", StringType(), True),
                                     StructField("time", StringType(), True),
                                     StructField("Method", StringType(), True),
                                     StructField("URI", StringType(), True),
                                     StructField("HTTP-Code", StringType(), True),
                                     StructField("code", StringType(), True),
                                     StructField("size", StringType(), True),
                                     StructField("device", StringType(), True),
                                     StructField("tenant_id", StringType(), True),
                                     StructField("timezone", StringType(), True),
                                     StructField("OS", StringType(), True),
                                     StructField("browser", StringType(), True),
                                     StructField("country", StringType(), True),
                                     StructField("screenResolution", StringType(), True),
                                     StructField("action", StringType(), True),
                                     StructField("referrer", StringType(), True),
                                     StructField("timeonpage", StringType(), True),
                                     StructField("supplier_id", StringType(), True),
                                     StructField("product", StringType(), True),
                                     StructField("geolocation", StringType(), True)])
                #
                # schema =['IP','user_identifier','user_id','user_name','time','Message','code',
                #  'size','device','user_name','tenant_id','timezone','OS', 'browser',
                #  'country','screenResolution','action','referrer','timezone',
                #  'supplier_id','product','geolocation']

                df = rdd.toDF(schema)
                df.write.mode("Overwrite").format('json').save("hdfs://localhost:9820/user/rzariwal/stream")

        # # Consume Kafka streams directly, without receivers
        lines = KafkaUtils.createDirectStream(ssc, [self.topic], {"metadata.broker.list": self.addr})
        lines1 = lines.map(lambda x: x[1])
        lines1.cache()
        val_sum_lines = lines1.window(self.report_interval, self.batch_interval)
        val_sum_lines_top_ip = val_sum_lines.filter(lambda x:  'HEARTBEAT' not in x) \
            .map(lambda x: (x.split(' ')[0].rstrip(' '), x.split(' ')[1].rstrip(' '), x.split(' ')[2].rstrip(' '), x.split(' ')[3].rstrip(' '), \
                            x.split(' ')[4].lstrip('['), x.split(' ')[6].lstrip('"'), x.split(' ')[7].rstrip(' '), \
                            x.split(' ')[8].rstrip('"'), x.split(' ')[9].rstrip(' '), x.split(' ')[10].rstrip(' '), \
                            x.split(' ')[11].rstrip(' '), x.split(' ')[12].rstrip(' '), x.split(' ')[13].rstrip(' '), \
                            x.split(' ')[14].rstrip(' '), x.split(' ')[15].rstrip(' '), x.split(' ')[16].rstrip(' '), \
                            x.split(' ')[17].rstrip(' '), x.split(' ')[18].rstrip(' '), x.split(' ')[19].rstrip(' '), \
                            x.split(' ')[20].rstrip(' '), x.split(' ')[21].rstrip(' '), x.split('[')[2].rstrip('] '), \
                            x.split('[')[3].rstrip('] ')))

        val_sum_lines_top_ip.foreachRDD(savetohdfs)
        val_sum_lines_top_ip1 = val_sum_lines_top_ip.map(lambda x: (x[3], x[4], x[6], x[8]))
        val_sum_lines_top_ip1.pprint()

        def savetheresult(rdd):
            if not rdd.isEmpty():
                hbase_table = 'flexigym'
                hconn = happybase.Connection('localhost')
                ctable = hconn.table(hbase_table)
                hconn.open()

                for row in rdd.collect():
                    time = datetime.now()
                    counter = str(time) + row[0]
                    ctable.put(counter, {b'Page_Visted:': row[2], b'Response_Code:': row[3], b'Time:': row[1], b'User_Name:': row[0]})

                schema = ["User_Name", "Page_Visted", "Response_Code", "Time"]
                rdd.toDF(schema).groupBy("User_Name", "Page_Visted", "Response_Code", "Time") \
                    .count() \
                    .show(truncate=False)

        val_sum_lines_top_ip1.foreachRDD(savetheresult)
        return ssc

    def run(self):
        #		self.functionToCreateContext()
        ssc = StreamingContext.getOrCreate(os.environ['VISORHOME']+'/src/kafka_monitor/checkpoint/', lambda: self.functionToCreateContext())
        ssc.start()
        ssc.awaitTermination()



if __name__=="__main__":
    # Load the configurations
    with open(os.environ['VISORHOME']+"/config/kafka_monitor.json") as config_file:
        config = json.load(config_file)

    # Load private email information
    with open(os.environ['VISORHOME']+"/config/private.json") as private_file:
        config_private = json.load(private_file)

    monitor = kafka_monitor(config, config_private)
    monitor.run()