import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost', port=5672))

channel = connection.channel()
channel.exchange_declare(exchange='amq.topic',
                         exchange_type='topic', durable=True)

def convertMessage(data):
    keys, values = '', ''
    for k, v in data.items():
      keys+=k+','
      values+=v+','
    return "%s\n%s"%(keys[:-1], values[:-1])

def sendMessage(body):
    channel.basic_publish(
            exchange='amq.topic',  #Usando amq.topic como exchange
            routing_key='hello',   #Routing key usada pelo produtor
            body=body
        )
    return "[X] Mensagem enviada com sucesso!"+body