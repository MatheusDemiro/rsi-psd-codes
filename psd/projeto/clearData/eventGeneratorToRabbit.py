import csv
import time
from projeto.clearData.sendMessageCsvToRabbit import sendMessage,connection

def publish(data):
    if data['tgn'] == "-":
        message = '{"ts": %d, "values":{"tbs": %.3f, "ur": %.3f, "tpo": %.3f}}' %(int(data['timestamp_pasto'])*1000, int(data['tbs'])/1000, int(data['ur'])/1000, int(data['tpo'])/1000)
    else:
        message = '{"ts": %d, "values":{"tbs": %.3f, "ur": %.3f, "tgn": %.3f, "tpo": %.3f}}' % (int(data['timestamp_pasto']) * 1000, int(data['tbs']) / 1000, int(data['ur']) / 1000,
                                                                                                int(data['tgn']) / 1000,int(data['tpo']) / 1000)
    print(sendMessage(message))

tabela_clima = open("arquivos/novos_arquivos/pasto.csv", "r")

try:
    data = csv.reader(tabela_clima, delimiter=";")
    columns = next(data)
    reference = dict(zip(columns, next(data)))
    current_timestamp = int(time.time())
    offset = current_timestamp - int(reference['timestamp_pasto'])
    for row in data:
        current_row = dict(zip(columns, row))
        while (int(current_row['timestamp_pasto']) + offset) > current_timestamp:
            time.sleep(1)
            current_timestamp += 60
        publish(current_row) #Publicando mensagem
finally:
    tabela_clima.close()
    connection.close() #Fechando conexao com o servidor rabbit