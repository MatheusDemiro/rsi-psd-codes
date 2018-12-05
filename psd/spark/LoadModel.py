import json

from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.types import *

#PATH_CSV = "/home/rsi-psd-vm/Documents/GitHub/rsi-psd-codes/psd/projeto/clearData/arquivos/novos_arquivos/data.csv"

# def saveFile(csv):
#     try:
#         arq = open(PATH_CSV, "w")
#         arq.write(csv)
#         arq.close()
#         return True
#     except Exception:
#         return False
#
# def convertColumn(df, names):
#     for name in names:
#         if name == 'ts':
#             df = df.withColumn(name, df[name].cast(IntegerType()))
#         else:
#             df = df.withColumn(name, df[name].cast(DoubleType()))
#     return df

def applyModel(data):
    #data = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(PATH_CSV)

    data.show() #linha teste

    randomForestModel = PipelineModel.read().load('/home/rsi-psd-vm/Documents/GitHub/rsi-psd-codes/psd/spark/model')

    predictions = randomForestModel.transform(data)

    predict = predictions.select("predictedLabel") #DataFrame

    result = predict.toJSON().map(lambda j: json.loads(j)).collect()

    return result[0]['predictedLabel']