# from pyspark.sql.types import StructType,StructField, StringType, IntegerType
# from pyspark.sql import SparkSession
import happybase, json
ip = '127.0.0.1'
jsondata = {'IP': ip}
print(json.dumps(jsondata))
line = """107.211.153.64 - 447 Tamatha [10/Apr/2021:22:23:53 -0700] "POST /view/136 HTTP/2.0" 200 2289 Iphone 1 IST MacOSX IE SG 640x480 payment GoogleAd 10 9 ['3', 'Add Supp Needs Bronze'] ['1.33989545035111', '103.746414934077']"""
print(line.split(' ')[0])
print(line.split(' ')[1].rstrip(' '))
print(line.split(' ')[2])
print(line.split(' ')[3])
print(line.split(' ')[4].lstrip('['))
print(line.split(' ')[6].lstrip('"'))
print(line.split(' ')[7])
print(line.split(' ')[8].rstrip('"'))
print(line.split(' ')[9])
print(line.split(' ')[10])
print(line.split(' ')[11])
print(line.split(' ')[12])
print(line.split(' ')[13])
print(line.split(' ')[14])
print(line.split(' ')[15])
print(line.split(' ')[16])
print(line.split(' ')[17])
print(line.split(' ')[18])
print(line.split(' ')[19])
print(line.split(' ')[20])
print(line.split(' ')[21])
print(line.split('[')[2].rstrip('] '))
print(line.split('[')[3].rstrip('] '))
# from datetime import datetime
# # spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
# #
# # data2 = [("James","/test.html",3000),
# #          ("Michael","/test1.html",4000),
# #          ("Robert","/test2.html",4000),
# #          ]
# #
# # schema = StructType([ \
# #     StructField("User_Name",StringType(),True), \
# #     StructField("Page_Visited",StringType(),True), \
# #     StructField("count", IntegerType(), True)
# #     ])
# #
# # df = spark.createDataFrame(data=data2,schema=schema)
# # df.printSchema()
# # df.show(truncate=False)
#
#
# hbase_table = 'flexigym'
# hconn = happybase.Connection('localhost')
# ctable = hconn.table(hbase_table)
# hconn.open()
# # print(hconn.tables())
# time = datetime.now()
# #
# # for key, data in ctable.scan():
# #     print(key, data)
# #
# # for row in df.rdd.collect():
# #     counter = str(time) + row[0]
# #     ctable.put(counter, {b'Page_Visted:': row[1], b'Response_Code:': b'200', b'Time:': b'10:10', b'User_Name:': row[0]})
# #
# #
# # ctable.put(counter, {b'Page_Visted:': b'/test1.html', b'Response_Code:': b'200', b'Time:': b'10:10', b'User_Name:': b'raj'})
#
# for key, data in ctable.scan():
#     print(key, data)
