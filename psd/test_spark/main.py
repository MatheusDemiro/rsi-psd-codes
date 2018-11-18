import findspark
from pyspark.ml.classification import LogisticRegression
from pyspark.sql import SparkSession

findspark.init("C:\\spark-2.4.0-bin-hadoop2.7\\")

spark = SparkSession.builder\
    .master("local")\
    .appName("Spark Demo")\
    .getOrCreate()

df = spark.read.format("csv").option("header","true").option("inferSchema","true").load("C:\\Users\\User\\Documents\\Arquivos_2018.2\\dados-psd-2018-2.csv")

df.select(df.columns).show()

#for i in df.collect():
#    print(i)