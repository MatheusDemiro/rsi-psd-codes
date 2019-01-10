import pika
import json
import paho.mqtt.client as mqtt

#Credenciais do thingsboard local
THINGSBOARD_HOST = '172.16.207.69'
ACCESS_TOKEN = 'RgfJz9s7aSbZGTo28xn5'

credentials = pika.PlainCredentials('mpsd', 'mpsd')
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost', 5672, 'psd-2018-2', credentials))
channel = connection.channel()

client = mqtt.Client()

#Adicionando access token
client.username_pw_set(ACCESS_TOKEN)

#Connectando ao ThingsBoard atraves da porta MQTT padrao e com 60 segundos de keepalive
client.connect(THINGSBOARD_HOST, 18830, 60)

client.loop_start()

channel.queue_declare(queue='pasto')

print (' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
    client.publish('v1/devices/me/telemetry', json.dumps(json.loads(body)), 1)
    print("[X] Mensagem enviada com sucesso!")

channel.basic_consume(callback,
                      queue='pasto',
                      no_ack=True)

channel.start_consuming()
