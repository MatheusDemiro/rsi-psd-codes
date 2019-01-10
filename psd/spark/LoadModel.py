import json

from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession
from pyspark.sql.types import *

def convertColumn(df, names):
    for name in names:
        if name == 'ts':
            df = df.withColumn(name, df[name].cast(IntegerType()))
        else:
            df = df.withColumn(name, df[name].cast(DoubleType()))
    return df

def applyModel(data):
    data = convertColumn(data, data.columns)

    data.show() #linha teste

    randomForestModel = PipelineModel.read().load('/home/rsi-psd-vm/Documents/GitHub/rsi-psd-codes/psd/spark/model')

    predictions = randomForestModel.transform(data)

    predict = predictions.select("predictedLabel") #DataFrame

    result = predict.toJSON().map(lambda j: json.loads(j)).collect()

    return result[0]['predictedLabel']