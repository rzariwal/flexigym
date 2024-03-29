from pyspark.sql.functions import col, explode
from pyspark import SparkContext
from pyspark.sql import SparkSession

from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator

sc = SparkContext
spark = SparkSession.builder.appName('Recommendations using explicit interests').getOrCreate()

# read input data
packages = spark.read.csv("../data/FlexiGYMPackages.csv", inferSchema=True, header=True)
ratings = spark.read.csv("../data/FlexiGYMRatings.csv", inferSchema=True, header=True)

ratings.show()
ratings.printSchema()

ratings = ratings. \
    withColumn('userId', col('userId').cast('integer')). \
    withColumn('packageId', col('packageId').cast('integer')). \
    withColumn('rating', col('rating').cast('float')). \
    drop('timestamp')

ratings.show()

# calculate data sparse
nominator = ratings.select("rating").count()
num_users = ratings.select("userId").distinct().count()
num_packages = ratings.select("packageId").distinct().count()
factor = num_users * num_packages

sparse_percent = (1.0 - (nominator * 1.0) / factor) * 100
print("The ratings dataframe is ", "%.2f" % sparse_percent + "% empty.")

# Interpret Data - Group data by userId, count ratings
userId_ratings = ratings.groupBy("userId").count().orderBy('count', ascending=False)
userId_ratings.show()

# Interpret Data - Group data by packageId, count ratings
packageId_ratings = ratings.groupBy("packageId").count().orderBy('count', ascending=False)
packageId_ratings.show()

# Split the Data - Create train data set and test data set
(train, test) = ratings.randomSplit([0.8, 0.2], seed=1234)
# Create ALS model
als = ALS(userCol="userId", itemCol="packageId", ratingCol="rating", nonnegative=True, implicitPrefs=False,
          coldStartStrategy="drop")

type(als)

# Define param_grid for Hyperparameter values to help tune the model
param_grid = ParamGridBuilder() \
    .addGrid(als.rank, [10, 50, 100, 150]) \
    .addGrid(als.regParam, [.01, .05, .1, .15]) \
    .build()
#             .addGrid(als.maxIter, [5, 50, 100, 200]) \

# Define evaluation metric RMSE
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
print("Num models to be tested: ", len(param_grid))

# Using CrossValidator class, build the cross validation pipeline
cv = CrossValidator(estimator=als, estimatorParamMaps=param_grid, evaluator=evaluator, numFolds=5)

# Confirming that cross validator was built
print(cv)

# To get Best Model and Best Model Parameters, fit the cross validator to the 'train' dataset
model = cv.fit(train)

# get best model from the cross validator model above
best_model = model.bestModel

# Details of the best model
print(type(best_model))

print("Rank:	", best_model._java_obj.parent().getRank())

print("MaxIter: ", best_model._java_obj.parent().getMaxIter())
print("RegParam:", best_model._java_obj.parent().getRegParam())

# Run model on test data
test_predictions = best_model.transform(test)
RMSE = evaluator.evaluate(test_predictions)
print("RMSE value is", "%.15f" % RMSE)

test_predictions.show()

n_recommendations = best_model.recommendForAllUsers(10)
n_recommendations.limit(10).show()

n_recommendations = n_recommendations \
    .withColumn("rec_exp", explode("recommendations")) \
    .select('userId', col("rec_exp.packageId"), col("rec_exp.rating"))

n_recommendations.limit(10).show()

n_recommendations.join(packages, on='packageId').filter('userId = 100').show()
ratings.join(packages, on='packageId').filter('userId = 100').sort('rating', ascending=False).limit(10).show()

# Save the model into cluster as files
als.save('../models/FlexiGYMExplicitRecommender_ALS')
model.save('../models/FlexiGYMExplicitRecommender_ALSModel')

