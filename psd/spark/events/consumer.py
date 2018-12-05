from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import ast
from mqtt import MQTTUtils

# spark = SparkSession.builder\
#     .master("local")\
#     .appName("Spark Demo")\
#     .getOrCreate()

def getSparkSessionInstance(sparkConf):
    if ('sparkSessionSingletonInstance' not in globals()):
        globals()['sparkSessionSingletonInstance'] = SparkSession\
            .builder\
            .config(conf=sparkConf)\
            .getOrCreate()
    return globals()['sparkSessionSingletonInstance']

def load(data):
    from spark.loadModel import applyModel
    return applyModel(data)

sc = SparkContext()
ssc = StreamingContext(sc, 10)

def process(time, rdd):
    print("========= %s =========" % str(time))

    try:
        # Get the singleton instance of SparkSession
        spark = getSparkSessionInstance(rdd.context.getConf())

        # Convert RDD[String] to RDD[Row] to DataFrame
        rowRdd = rdd.map(lambda w: Row(word=w))
        wordsDataFrame = spark.createDataFrame(rowRdd)

        # Creates a temporary view using the DataFrame.
        wordsDataFrame.createOrReplaceTempView("words")

        # Do word count on table using SQL and print it
        wordCountsDataFrame = \
            spark.sql("select word, count(*) as total from words group by word")
        wordCountsDataFrame.show()
    except:
        pass

mqttStream = MQTTUtils.createStream(
    ssc, 
    "tcp://localhost:1883",  # Note both port number and protocol
    "hello"                  # The same routing key as used by producer
)

#counts = mqttStream.map(lambda line: load(ast.literal_eval(line)))

#counts = mqttStream.map(lambda line: load(line))

features = mqttStream.map(lambda  l: l.split(","))

featureRDD = features.foreachRDD(process)

#applyModel(#Caminho do arquivo csv)

ssc.start()
ssc.awaitTermination()
ssc.stop()
