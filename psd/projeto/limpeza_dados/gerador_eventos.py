import csv
import time
from datetime import datetime, timedelta
from send_message import sendMessage,connection

def publish(data):
    message = "timestamp_pasto: %s; tbs: %s; ur: %s; tgn: %s; tpo: %s" %(data['timestamp_pasto'], data['tbs'], data['ur'], data['tgn'],
                                                                        data['tpo'])
    print(sendMessage(message))

tabela_clima = open("arquivos/pasto2.csv", "r")

try:
    data = csv.reader(tabela_clima, delimiter=";")
    columns = next(data)
    reference = dict(zip(columns, next(data)))
    current_timestamp = int(time.time())
    offset = current_timestamp - int(reference['timestamp_pasto'])
    for row in data:
        current_row = dict(zip(columns, row))
        current_timestamp = int(time.time())
        while (int(current_row['timestamp_pasto']) + offset) > current_timestamp:
            time.sleep(1)
            temp = datetime.fromtimestamp(current_timestamp) + timedelta(minutes=60) #Convertendo timestamp para o formato datetime e acrescentando 60 minutos
            current_timestamp = datetime.timestamp(temp)
        publish(current_row) #Publicando mensagem
finally:
    tabela_clima.close()
    connection.close() #Fechando conexao com o servidor rabbit