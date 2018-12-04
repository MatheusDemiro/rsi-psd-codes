import csv
from pyspark.ml import PipelineModel
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = SparkSession.builder\
    .master("local")\
    .appName("Spark Demo")\
    .getOrCreate()

def convertCSV(dictionary):
    # keys, values = '', ''
    # for k, v in dictionary.items():
    #   keys+=k+','
    #   values+=v+','
    # return "%s\n%s"%(keys[:-1], values[:-1])
    path = '/home/rsi-psd-vm/Documents/GitHub/rsi-psd-codes/psd/projeto/clearData/arquivos/novos_arquivos/data.csv'
    keys = dictionary.keys()
    with open(path,'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows([dictionary])
    return path

def convertColumn(df, names):
    for name in names:
        if name == 'ts':
            df = df.withColumn(name, df[name].cast(IntegerType()))
        else:
            df = df.withColumn(name, df[name].cast(DoubleType()))
    return df

#pathOrigin = "/home/rsi-psd-vm/Documents/GitHub/rsi-psd-codes/psd/projeto/clearData/arquivos/novos_arquivos/dados_finais.csv"

def applyModel(dictionary):
    #converter dicionário em csv
    path_csv = convertCSV(dictionary)

    data = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(path_csv)

    data = convertColumn(data, data.columns[:-1])

    data.show() #linha teste

    randomForestModel = PipelineModel.read().load('/home/rsi-psd-vm/Documents/GitHub/rsi-psd-codes-master/psd/spark/model')

    predictions = randomForestModel.transform(data)

    #predictions.select("predictedLabel", "classe", "features").show(287, False)

    predictions.select("predictedLabel").show() #DataFrame

    return "OI"

    # evaluator = MulticlassClassificationEvaluator(
    #     labelCol="indexedLabel", predictionCol="prediction", metricName="accuracy")
    # accuracy = evaluator.evaluate(predictions)
    #
    # print("Test Accuracy Rate: %g\nTest Error Rate: %g" % (accuracy, 1.0 - accuracy))
    #
    # rfModel = randomForestModel.stages[2]
    # print(rfModel)