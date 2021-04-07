from pyspark.ml.recommendation import ALS, ALSModel
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName('Load model for Recommendations using explicit interests').getOrCreate()

#Load saved als and model
als = ALS.load('../models/FlexiGYMExplicitRecommender_ALS')
model = ALSModel.load('../models/FlexiGYMExplicitRecommender_ALSModel/bestModel')

print(als.getMaxIter())
print(model.userFactors.collect())
print(model.itemFactors.collect())