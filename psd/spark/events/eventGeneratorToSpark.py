import csv
import time
from spark.events.sendMessageSparkToRabbit import sendMessage, connection

data_table = open("/home/rsi-psd-vm/Documents/GitHub/rsi-psd-codes/psd/projeto/clearData/arquivos/novos_arquivos/dados_finais.csv", "r")

try:
    data = csv.reader(data_table, delimiter=";")
    next(data)
    for row in data:
        time.sleep(15)
        print(sendMessage(",".join(row[0].split(",")[:-1])))  # Publicando mensagem
finally:
    data_table.close()
    connection.close()  #Fechando conexao com o servidor rabbit
