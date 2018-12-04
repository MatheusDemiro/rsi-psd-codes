import datetime
import time
import csv

cassandra2 = open("arquivos/Cassandra2.TXT","r+")

data = cassandra2.readlines()

cassandra2.close()

with open('arquivos/novos_arquivos/cassandra2.csv', 'w', newline='') as csvfile:
    #Parametros de configuracao do csv. O parametro 'csv.QUOTE_MINIMAL' serve para o gravador focar apenas nos campos que contem caracteres especiais como os delimitadores
    spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL) 
    spamwriter.writerow(['Timestamp', 'Latitude', 'Longitude']) #Rótulos das colunas
    for information in data:
        temp = information.replace("|\n","").split(" - ")
        temp = temp[1].split(" | ") #Cortar a lista apenas com os columns de interesse (data e hora) para formar o timestamp
        if temp[0] == "0/0" or temp[0] == "0/36":
            continue        
        temp[0] = temp[0]+"/2016" #Adicionando o ano de 2016
        date = [temp[0],temp[1]]
        timestamp = str(int(time.mktime(datetime.datetime.strptime(" ".join(date), "%d/%m/%Y %H:%M:%S").timetuple())))
        spamwriter.writerow([timestamp,temp[2], temp[3]])
'''
#Reverse engineering

from datetime import datetime

a = open("arquivos/newCassandra2.txt","r")

b = a.readlines()

a.close()

for i in b:
    print(datetime.utcfromtimestamp(int(i[0:-1])).strftime('%d/%m/%Y %H:%M:%S'))
'''
