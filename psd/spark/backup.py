import findspark
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer, VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import SparkSession
from pyspark.sql.types import *

def convertColumn(df, names, newType):
    for name in names:
        if name == 'ts':
            df = df.withColumn(name, df[name].cast(IntegerType()))
        else:
            df = df.withColumn(name, df[name].cast(newType))
    return df

findspark.init("C:\spark-2.4.0-bin-hadoop2.7")

spark = SparkSession.builder\
    .master("local")\
    .appName("Spark Demo")\
    .getOrCreate()

data = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("C:\Users\User\Documents\UFRPE\Arquivos_2018.2\dados-psd-2018-2.csv")

data = convertColumn(data, data.columns[:-1], DoubleType())

vecAssembler = VectorAssembler(inputCols=data.columns[:-1], outputCol="features").setHandleInvalid("keep")

labelIndexer = StringIndexer(inputCol="classe", outputCol="indexedLabel").fit(data)

featureIndexer = VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4)

(trainingData, testData) = data.randomSplit([0.7, 0.3])

rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", numTrees=100)

labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",
                               labels=labelIndexer.labels)

pipeline = Pipeline(stages=[vecAssembler, labelIndexer, featureIndexer, rf, labelConverter])

model = pipeline.fit(trainingData)

predictions = model.transform(testData)

predictions.select("predictedLabel", "classe", "features").show(5)

evaluator = MulticlassClassificationEvaluator(
    labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test Error = %g" % (1.0 - accuracy))

rfModel = model.stages[2]
print(rfModel)
#for i in data.collect():
#    print(i)