from pyspark.sql.functions import col, explode
from pyspark import SparkContext
from pyspark.sql import SparkSession

from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator


sc = SparkContext
# sc.setCheckpointDir('checkpoint')
spark = SparkSession.builder.appName('Recommendations using explicit interests').getOrCreate()

#read data
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

#Check data sparsity
numerator = ratings.select("rating").count()
num_users = ratings.select("userId").distinct().count()
num_packages = ratings.select("packageId").distinct().count()
denominator = num_users * num_packages

sparsity = (1.0 - (numerator * 1.0) / denominator) * 100
print("The ratings dataframe is ", "%.2f" % sparsity + "% empty.")

# Interpret ratings
# Group data by userId, count ratings
userId_ratings = ratings.groupBy("userId").count().orderBy('count', ascending=False)
userId_ratings.show()

# Group data by packageId, count ratings
packageId_ratings = ratings.groupBy("packageId").count().orderBy('count', ascending=False)
packageId_ratings.show()

# Create test and train set
(train, test) = ratings.randomSplit([0.8, 0.2], seed=1234)
# Create ALS model
als = ALS(userCol="userId", itemCol="packageId", ratingCol="rating", nonnegative=True, implicitPrefs=False,
          coldStartStrategy="drop")

# Confirm that a model called "als" was created
type(als)

#Inform Spark how to tune your ALS model
# Add hyperparameters and their respective values to param_grid
param_grid = ParamGridBuilder() \
    .addGrid(als.rank, [10, 50, 100, 150]) \
    .addGrid(als.regParam, [.01, .05, .1, .15]) \
    .build()
#             .addGrid(als.maxIter, [5, 50, 100, 200]) \

# Define evaluator as RMSE and print length of evaluator
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
print("Num models to be tested: ", len(param_grid))

#Build your cross validation pipeline
# Build cross validation using CrossValidator
cv = CrossValidator(estimator=als, estimatorParamMaps=param_grid, evaluator=evaluator, numFolds=5)

# Confirm cv was built
print(cv)

#Best Model and Best Model Parameters
# Fit cross validator to the 'train' dataset
model = cv.fit(train)

# best model from the cv model above
best_model = model.bestModel

#Best model details
print(type(best_model))

print("Rank:	", best_model._java_obj.parent().getRank())

print("MaxIter: ", best_model._java_obj.parent().getMaxIter())
print("RegParam:", best_model._java_obj.parent().getRegParam())

# Run model on test data
test_predictions = best_model.transform(test)
RMSE = evaluator.evaluate(test_predictions)
print(RMSE)

test_predictions.show()


nrecommendations = best_model.recommendForAllUsers(10)
nrecommendations.limit(10).show()

nrecommendations = nrecommendations \
    .withColumn("rec_exp", explode("recommendations")) \
    .select('userId', col("rec_exp.packageId"), col("rec_exp.rating"))

nrecommendations.limit(10).show()

nrecommendations.join(packages, on='packageId').filter('userId = 100').show()
ratings.join(packages, on='packageId').filter('userId = 100').sort('rating', ascending=False).limit(10).show()

#Save the model
als.save('../models/FlexiGYMExplicitRecommender_ALS')
model.save('../models/FlexiGYMExplicitRecommender_ALSModel')

