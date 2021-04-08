from pyspark.sql.types import StructType,StructField, StringType, IntegerType
from pyspark.sql import SparkSession
import happybase
from datetime import datetime
# spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()
#
# data2 = [("James","/test.html",3000),
#          ("Michael","/test1.html",4000),
#          ("Robert","/test2.html",4000),
#          ]
#
# schema = StructType([ \
#     StructField("User_Name",StringType(),True), \
#     StructField("Page_Visited",StringType(),True), \
#     StructField("count", IntegerType(), True)
#     ])
#
# df = spark.createDataFrame(data=data2,schema=schema)
# df.printSchema()
# df.show(truncate=False)


hbase_table = 'flexigym'
hconn = happybase.Connection('localhost')
ctable = hconn.table(hbase_table)
hconn.open()
# print(hconn.tables())
time = datetime.now()
#
# for key, data in ctable.scan():
#     print(key, data)
#
# for row in df.rdd.collect():
#     counter = str(time) + row[0]
#     ctable.put(counter, {b'Page_Visted:': row[1], b'Response_Code:': b'200', b'Time:': b'10:10', b'User_Name:': row[0]})
#
#
# ctable.put(counter, {b'Page_Visted:': b'/test1.html', b'Response_Code:': b'200', b'Time:': b'10:10', b'User_Name:': b'raj'})

for key, data in ctable.scan():
    print(key, data)
