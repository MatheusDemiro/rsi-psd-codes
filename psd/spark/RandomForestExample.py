import findspark
from pyspark.ml import Pipeline
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.feature import IndexToString, StringIndexer, VectorIndexer, VectorAssembler
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import SparkSession
from pyspark.sql.types import *

findspark.init("C:\spark-2.4.0-bin-hadoop2.7")

class RandomForest():

    def __init__(self):
        pass

    def getContext(self):
        spark = SparkSession.builder \
            .master("local") \
            .appName("Spark Demo") \
            .getOrCreate()

        return spark

    def generateData(self):
        spark_context = self.getContext()

        data = spark_context.read.format("csv").option("header", "true").option("inferSchema", "true").load(
            "C:\Users\User\Documents\UFRPE\Arquivos_2018.2\dados-psd-2018-2.csv")

        data = self.convertColumn(data, data.columns[:-1])

        return data

    def convertColumn(self, dataframe, columns):
        for name in columns:
            if name == 'ts':
                dataframe = dataframe.withColumn(name, dataframe[name].cast(IntegerType()))
            else:
                dataframe = dataframe.withColumn(name, dataframe[name].cast(DoubleType()))
        return dataframe

    def randomForestClassifier(self, data, trainingData):
        print(data)
        vecAssembler = VectorAssembler(inputCols=data.columns[:-1], outputCol="features").setHandleInvalid("keep")

        labelIndexer = StringIndexer(inputCol="classe", outputCol="indexedLabel").fit(data)

        featureIndexer = VectorIndexer(inputCol="features", outputCol="indexedFeatures", maxCategories=4)

        rf = RandomForestClassifier(labelCol="indexedLabel", featuresCol="indexedFeatures", numTrees=100)

        labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel",
                                       labels=labelIndexer.labels)

        pipeline = Pipeline(stages=[vecAssembler, labelIndexer, featureIndexer, rf, labelConverter])

        return pipeline.fit(trainingData)

    def getAcurrancy(self, predictions):
        evaluator = MulticlassClassificationEvaluator(
            labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
        return evaluator.evaluate(predictions)