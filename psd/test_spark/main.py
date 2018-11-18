import findspark
from pyspark.sql import SparkSession

findspark.init("C:\\spark-2.4.0-bin-hadoop2.7\\")

spark = SparkSession.builder\
    .master("local")\
    .appName("Spark Demo")\
    .getOrCreate()

#df = spark.read.format("image").option("dropInvalid", "true").load("C:\spark-2.4.0-bin-hadoop2.7\data\mllib\images\origin\kittens")

#df.select("image.origin", "image.width", "image.height").show(truncate=False)
df = spark.read.format("csv").option("header","true").option("inferSchema","true").load("C:\\Users\\User\\Documents\\Arquivos_2018.2\\pasto.csv")

df.select(df.columns).show()

#print(df)
#df.printSchema()
#for i in df.collect():
#    print(i)