from pyspark.ml import PipelineModel
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

spark = SparkSession.builder\
    .master("local")\
    .appName("Spark Demo")\
    .getOrCreate()

data = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("/home/rsi-psd-vm/Documents/GitHub/rsi-psd-codes-master/psd/projeto/limpeza_dados/arquivos/novos_arquivos/dados_finais.csv")

data = convertColumn(data, data.columns[:-1])

path = "/home/rsi-psd-vm/Documents/GitHub/rsi-psd-codes-master/psd/spark/model"

randomForestModel = PipelineModel.read().load(path)

predictions = randomForestModel.transform(data)

predictions.select("predictedLabel", "classe", "features").show(287, False)

evaluator = MulticlassClassificationEvaluator(
    labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Test Accuracy Rate: %g\nTest Error Rate: %g" % (accuracy, 1.0 - accuracy))

rfModel = randomForestModel.stages[2]
print(rfModel)