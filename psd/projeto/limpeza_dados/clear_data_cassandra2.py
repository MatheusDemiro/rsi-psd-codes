import datetime
import time
import csv

def formatTimestamp(array): #Converter array com horario para string
    hour = array[1][0:2]
    if len(array[0].split("/")[0]) == 1:
        array[0] = "0"+array[0]
    if hour == "00":
        time = "21"
        array[0] = array[0].replace(array[0][0:2], str(int(array[0][0:2])-1))           
    elif hour == "01":
        time = "22"
        array[0] = array[0].replace(array[0][0:2], str(int(array[0][0:2])-1))
    elif hour == "02":
        time = "23"
        array[0] = array[0].replace(array[0][0:2], str(int(array[0][0:2])-1))
    else:
         time = str(int(hour))
    return array[0]+" "+time+array[1][2:]

cassandra2 = open("arquivos/Cassandra2.TXT","r+")

data = cassandra2.readlines()

cassandra2.close()

with open('arquivos/Cassandra2.csv', 'w', newline='') as csvfile:
    #Parametros de configuracao do csv. O parametro 'csv.QUOTE_MINIMAL' serve para o gravador focar apenas nos campos que contem caracteres especiais como os delimitadores
    spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL) 
    spamwriter.writerow(['Timestamp', 'Latitude', 'Longitude']) #Rótulos das colunas
    for information in data:
        temp = information.replace("|\n","").split(" - ")
        temp = temp[1].split(" | ") #Cortar a lista apenas com os dados de interesse (hora e data) para formar o timestamp
        if temp[0] == "0/0" or temp[0] == "0/36":
            continue        
        temp[0] = temp[0]+"/2018" #Adicionando o ano de 2018
        timestamp = str(int(time.mktime(datetime.datetime.strptime(formatTimestamp(temp), "%d/%m/%Y %H:%M:%S").timetuple())))
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
