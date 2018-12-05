import pika
import ast

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
# credentials = pika.PlainCredentials('vwcm', 'vwcm')
# connection = pika.BlockingConnection(pika.ConnectionParameters(
#               'localhost', 5672, 'psd', credentials))
channel = connection.channel()
channel.exchange_declare(exchange='amq.topic',
                         exchange_type='topic', durable=True)

def convertMessage(data):
    keys, values = '', ''
    for k, v in data.items():
      keys+=k+','
      values+=v+','
    return "%s\n%s"%(keys[:-1], values[:-1])

def sendMessage(dictionary):
    body = convertMessage(ast.literal_eval(dictionary)) #Passando dict como parâmetro
    channel.basic_publish(
            exchange='amq.topic',  # amq.topic as exchange
            routing_key='hello',   # Routing key used by producer
            body=body
        )
    return "[X] Mensagem enviada com sucesso!"+dictionary