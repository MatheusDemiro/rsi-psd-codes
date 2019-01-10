import findspark
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer, VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import SparkSession
from pyspark.sql.types import *

def convertColumn(df, names):
    for name in names:
        if name == 'ts':
            df = df.withColumn(name, df[name].cast(IntegerType()))
        else:
            df = df.withColumn(name, df[name].cast(DoubleType()))
    return df

findspark.init("/home/rsi-psd-vm/spark-2.4.0-bin-hadoop2.7")

spark = SparkSession.builder\
    .master("local")\
    .appName("Spark Demo")\
    .getOrCreate()

data = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("/home/rsi-psd-vm/Documents/GitHub/rsi-psd-codes/psd/projeto/clearData/arquivos/novos_arquivos/dados_finais.csv")

data = convertColumn(data, data.columns[:-1])

vecAssembler = VectorAssembler(inputCols=data.columns[:-1], outputCol="features").setHandleInvalid("keep")

labelIndexer = StringIndexer(inputCol="classe", outputCol="indexedLabel").fit(data)

featureIndexer = VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4)

(trainingData, testData) = data.randomSplit([0.7, 0.3])

randomForestClassifier = RandomForestClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", numTrees=100)

labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",
                               labels=labelIndexer.labels)

pipeline = Pipeline(stages=[vecAssembler, labelIndexer, featureIndexer, randomForestClassifier, labelConverter])

randomForestModel = pipeline.fit(trainingData)

randomForestModel.write().overwrite().save("/home/rsi-psd-vm/Documents/GitHub/rsi-psd-codes/psd/spark/model")

predictions = randomForestModel.transform(testData)

predictions.select("predictedLabel", "classe", "features").show(5)

evaluator = MulticlassClassificationEvaluator(
    labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test Accuracy Rate: %g\nTest Error Rate: %g" % (accuracy, 1.0 - accuracy))

rfModel = randomForestModel.stages[2]
print(rfModel)