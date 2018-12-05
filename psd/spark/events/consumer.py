from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import ast
from mqtt import MQTTUtils

def load(data):
    from spark.loadModel import applyModel
    return applyModel(data)

sc = SparkContext()
ssc = StreamingContext(sc, 10)

mqttStream = MQTTUtils.createStream(
    ssc, 
    "tcp://localhost:1883",  # Note both port number and protocol
    "hello"                  # The same routing key as used by producer
)

#counts = mqttStream.map(lambda line: load(ast.literal_eval(line)))

counts = mqttStream.map(lambda line: load(line))

counts.pprint()

#applyModel(#Caminho do arquivo csv)

ssc.start()
ssc.awaitTermination()
ssc.stop()
