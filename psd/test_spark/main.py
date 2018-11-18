import findspark
from pyspark.sql import SparkSession
from pyspark.sql.types import *

def convertColumn(df, names, newType):
    for name in names:
        if name == 'ts':
            df = df.withColumn(name, df[name].cast(IntegerType()))
        else:
            df = df.withColumn(name, df[name].cast(newType))
    return df

findspark.init("C:\\spark-2.4.0-bin-hadoop2.7\\")

spark = SparkSession.builder\
    .master("local")\
    .appName("Spark Demo")\
    .getOrCreate()

data = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load("C:\\Users\\User\\Documents\\Arquivos_2018.2\\dados-psd-2018-2.csv")

new_data = convertColumn(data,data.columns[:-1],DoubleType())

new_data.show()

print(new_data.dtypes)

#for i in data.collect():
#    print(i)