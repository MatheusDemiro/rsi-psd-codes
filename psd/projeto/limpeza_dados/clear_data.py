import datetime
import time

def formatTimestamp(array):
    hour = array[1][0:2]
    if hour == "00":
        time = "21"
    elif hour == "01":
        time = "22"
    elif hour == "02":
        time = "23"
    else:
        time = str(int(hour)-2)
    print(array[0]+" "+time+array[1][2:])
    return array[0]+" "+time+array[1][2:]

cassandra2 = open("Cassandra2.TXT","r+")
newCassandra2 = open("newCassandra2.txt","w+")

data = cassandra2.readlines()

cassandra2.close()

#Falta condicao para hora "00","01" e "02", pois como subtraimos 3 para seguir o padrao UTC a hora fica com valor negativo.
#Verificar se as condição para as datas "0/0" estão funcionais


for information in data:
    temp = information.split(" - ")
    temp = temp[1].split(" | ") #Cortar a lista apenas com os dados de interesse (hora e data) para formar o timestamp
    if temp[0] == "0/0" or temp[0] == "0/36":
        continue        
    temp[0] = temp[0]+"/2018" #Adicionando o ano de 2018
    newCassandra2.writelines(str(int(time.mktime(datetime.datetime.strptime(formatTimestamp(temp), "%d/%m/%Y %H:%M:%S").timetuple())))+"\n")
newCassandra2.close()
'''
#Reverse engineering

from datetime import datetime

a = open("newCassandra2.txt","r")

b = a.readlines()

a.close()

for i in b:
    print(datetime.utcfromtimestamp(int(i[0:-1])).strftime('%d/%m/%Y %H:%M:%S'))
'''
