import csv
import datetime
import time

newTable = open("arquivos/novos_arquivos/sombra.csv", "w", newline='') #Arquivo aberto no modo de escrita
table = open("arquivos/sombra_formatado.csv", "r") #Arquivo aberto no modo de leitura
try:
    data = csv.reader(table)
    columns = next(data) #Pulando primeira row
    record = csv.writer(newTable, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    record.writerow(['timestamp_abrigo', 'tbs', 'ur', 'tgn', 'tpo']) #Rotulos das colunas
    for row in data:
        temp = row[0].split(";")
        if temp[0] != '':
            date = " ".join(temp[0].replace("h",":").replace("min",":").replace("s","").split())
            timestamp = str(int(time.mktime(datetime.datetime.strptime(date, "%m/%d/%Y %H:%M:%S").timetuple())))
            temp[0] = timestamp
            record.writerow(temp)
finally:
    table.close()
    newTable.close()
