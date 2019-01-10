import csv
import datetime
import time

newTable = open("arquivos/novos_arquivos/pasto.csv", "w", newline='')  #Arquivo aberto no modo de escrita
table = open("arquivos/pasto_formatado.csv", "r")  #Arquivo aberto no modo de leitura

try:
    data = csv.reader(table)
    columns = next(data)[0].split(";") #Pulando os rotulos das colunas
    record = csv.writer(newTable, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    record.writerow(['timestamp_abrigo', columns[1], columns[2], columns[3], columns[4]])  #Rotulos das colunas
    for row in data:
        temp = row[0].split(";")
        if temp[0] != "":
            temp[0] = temp[0].replace("h", ":").replace("min", ":").replace("s", "") #Trocando os elementos inconsistentes
            timestamp = str(int(time.mktime(datetime.datetime.strptime(temp[0], "%m/%d/%Y %H:%M:%S").timetuple())))
            temp[0] = timestamp
            if temp[3] == '':
                temp[3] = "-"
            record.writerow(temp)
finally:
    table.close()
    newTable.close()