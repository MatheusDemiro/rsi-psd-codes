#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('mpsd', 'mpsd')
connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost', 5672, 'psd-2018-2', credentials))

def sendMessage(message):
    channel = connection.channel()

    channel.queue_declare(queue='pasto')

    channel.basic_publish(exchange='',
                          routing_key='pasto',
                          body=message)

    return "[x] Mensagem enviada com sucesso!"
