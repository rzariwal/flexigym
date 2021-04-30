from pyspark.sql.functions import col, explode
from pyspark import SparkContext
from pyspark.sql import SparkSession

from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator

sc = SparkContext
spark = SparkSession.builder.appName('Recommendations using implicit interests').getOrCreate()

# read input data
packages = spark.read.csv("../data/FlexiGYMPackages.csv", inferSchema=True, header=True)
ratings_orig = spark.read.csv("../data/FlexiGYMPackageViews.csv", inferSchema=True, header=True)

#ratings = ratings.groupBy(['userId','packageId']).count().withColumnRenamed("count", "viewScore")

ratings = ratings_orig.groupBy(['userId','packageId','event_type']).count().withColumnRenamed("count", "rating")
ratings.show()
ratings.printSchema()

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
(train, test) = ratings.randomSplit([0.7, 0.3], seed=56)
# Create ALS model
als = ALS(userCol="userId", itemCol="packageId", ratingCol="rating", nonnegative=True, implicitPrefs=True,
          coldStartStrategy="drop")

type(als)

# Define param_grid for Hyperparameter values to help tune the model
param_grid = ParamGridBuilder() \
    .addGrid(als.rank, [100]) \
    .addGrid(als.regParam, [.1]) \
    .addGrid(als.maxIter, [1]) \
    .build()

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

n_recommendations_550031373 = n_recommendations.join(packages, on='packageId').filter('userId = 550031373')

print("category of recommended items for n_recommendations_550031373")
n_recommendations_550031373.join(ratings_orig, on='packageId').filter(ratings_orig.userId == '550031373').limit(100).show()


print("category of original score items before recommendation for 550031373")
ratings_orig.join(packages, on='packageId').filter(ratings_orig.userId == '550031373').limit(100).show()



# Save the model into cluster as files
als.save('../models/FlexiGYMImplicitRecommender_ALS')
model.save('../models/FlexiGYMImplicitRecommender_ALSModel')

