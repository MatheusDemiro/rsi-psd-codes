import json
from pyspark import SparkContext
from pyspark.sql import SparkSession, Row
from pyspark.sql.types import *
from pyspark.streaming import StreamingContext
from pyspark.ml import PipelineModel
import paho.mqtt.client as mqttClient
from mqtt import MQTTUtils

THINGSBOARD_HOST = 'demo.thingsboard.io'
ACCESS_TOKEN = 'hCdT7t6jvbAh4KuU0wq0'

def getSparkSessionInstance(sparkConf):
    if ('sparkSessionSingletonInstance' not in globals()):
        globals()['sparkSessionSingletonInstance'] = SparkSession\
            .builder\
            .config(conf=sparkConf)\
            .getOrCreate()
    return globals()['sparkSessionSingletonInstance']

def convertColumn(df, names):
    for name in names:
        if name == 'ts':
            df = df.withColumn(name, df[name].cast(IntegerType()))
        else:
            df = df.withColumn(name, df[name].cast(DoubleType()))
    return df

def applyModel(data):
    data = convertColumn(data, data.columns)

    randomForestModel = PipelineModel.read().load('/home/rsi-psd-vm/Documents/GitHub/rsi-psd-codes/psd/spark/model')

    predictions = randomForestModel.transform(data)

    predict = predictions.select("predictedLabel", "lat", "local", "long", "posicao", "tbs_pasto", "tgn_pasto", "tpo_pasto", "ur_pasto", "tbs_sombra", "tgn_sombra", "tpo_sombra", "ur_sombra") #DataFrame

    predict.show()

    result = predict.toJSON().map(lambda j: json.loads(j)).collect()

    return result[0]

if __name__ == "__main__":
    sc = SparkContext()
    ssc = StreamingContext(sc, 10)

    mqttStream = MQTTUtils.createStream(
        ssc,
        "tcp://localhost:1883",  #Numero da porta e protocolo
        "hello"                  #Routing key usada pelo produtor
    )

    features = mqttStream.map(lambda l: l.split(","))

    def process(time, rdd):
        print("========= %s =========" % str(time))

        try:
            #Criando instancia singleton do SparkSession
            spark = getSparkSessionInstance(rdd.context.getConf())

            #Convertendo RDD[String] para RDD[Row]
            rowRDD = rdd.map(lambda p: Row(ts=p[0],lat=p[1],long=p[2],tbs_pasto=p[3],ur_pasto=p[4],
                                                     tgn_pasto=p[5],tpo_pasto=p[6],tbs_sombra=p[7],ur_sombra=p[8],
                                                     tgn_sombra=p[9],tpo_sombra=p[10],posicao=p[11],local=p[12]))
            #Montando Dataframe
            featuresDataFrame = spark.createDataFrame(rowRDD)

            sendTB(applyModel(featuresDataFrame))

        except Exception as e:
            print(e.args)
            pass

    def sendTB(state):
        client = mqttClient.Client()

        #Adicionando o access token
        client.username_pw_set(ACCESS_TOKEN)

        #Connectando ao ThingsBoard atraves da porta MQTT padrao e com 60 segundos de keepalive
        client.connect(THINGSBOARD_HOST, 1883, 60)

        client.loop_start()

        client.publish('v1/devices/me/telemetry', json.dumps(state), 1)
        print("[X] Mensagem enviada com sucesso!")

    features.foreachRDD(process)

    ssc.start()
    ssc.awaitTermination()
    ssc.stop()
