from pyspark.ml.classification import NaiveBayes
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import SparkSession
import findspark

findspark.init("C:\\spark-2.4.0-bin-hadoop2.7\\")

spark = SparkSession.builder\
    .master("local")\
    .appName("Spark Demo")\
    .getOrCreate()

data = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("C:\\Users\\User\\Documents\\Arquivos_2018.2\\dados-psd-2018-2.csv")

splits = data.randomSplit([0.6, 0.4])

train = splits[0]
test = splits[1]

nb = NaiveBayes(smoothing=1.0, modelType="multinomial")

model = nb.fit(train)

predictions = model.transform(test)
predictions.show()

evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction",
                                              metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test set accuracy = " + str(accuracy))