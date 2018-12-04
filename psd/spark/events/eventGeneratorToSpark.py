import csv
import time
from spark.events.sendMessageSparkToRabbit import sendMessage, connection

data_table = open("/home/rsi-psd-vm/Documents/GitHub/rsi-psd-codes/psd/projeto/clearData/arquivos/novos_arquivos/dados_finais.csv", "r")

try:
    data = csv.reader(data_table, delimiter=";")
    columns = next(data)[0].split(",")[:-1]
    for row in data:
        print(sendMessage(str(dict(zip(columns, row[0].split(",")[:-1])))))  # Publicando mensagem
        time.sleep(15)
finally:
    data_table.close()
    connection.close()  # Fechando conexao com o servidor rabbit
