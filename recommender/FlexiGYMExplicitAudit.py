from pyspark.sql import SparkSession
from PySparkAudit import auditing

spark = SparkSession.builder.appName("FlexiGYMExplicitAudit.py").getOrCreate()

audit_folder_ratings = '../audit/FlexiGYMExplicitAudit/FlexiGYMRatings'

FlexiGYMExplicitDataRatings = spark.read.csv("../data/FlexiGYMRatings.csv", inferSchema=True, header=True)

auditing(FlexiGYMExplicitDataRatings, output_dir=audit_folder_ratings, tracking=True)

audit_folder_packages = '../audit/FlexiGYMExplicitAudit/FlexiGYMPackages'

FlexiGYMExplicitDataPackages = spark.read.csv("../data/FlexiGYMPackages.csv", inferSchema=True, header=True)

auditing(FlexiGYMExplicitDataPackages, output_dir=audit_folder_packages, tracking=True)


