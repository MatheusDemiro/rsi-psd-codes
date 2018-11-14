import datetime
import time
import csv

<<<<<<< HEAD:psd/projeto/limpeza_dados/clear_data_cassandra2.py
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
=======
def formatTimestamp(array):
    hour = str(int(array[1][0:2])-3)
    string = array[0]+" "+hour+array[1][2:]

    return string
>>>>>>> develop:psd/projeto/limpeza_dados/clear_data.py

cassandra2 = open("arquivos/Cassandra2.TXT","r+")

data = cassandra2.readlines()

cassandra2.close()

<<<<<<< HEAD:psd/projeto/limpeza_dados/clear_data_cassandra2.py
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
=======
aux = []

#Falta condicao para hora "00","01" e "02", pois como subtraimos 3 para seguir o padrao UTC a hora fica com valor negativo.
#Verificar se as condição para as datas "0/0" estão funcionais

for information in data:
    temp = information.split(" - ")
    temp = temp[1].split(" | ") #Cortar a lista apenas com os dados de interesse (hora e data) para formar o timestamp
    if temp[0] == "0/0":
        temp[0] = aux[-1] #Adicionando a ultima data adicionada
        print(temp[0])
    else:
        temp[0] = temp[0]+"/2018" #Adicionando o ano de 2018
        if temp[0] not in aux: #Minimizando o comprimento da lista auxiliar
            aux.append(temp[0])#Guardando a data para o caso de datas 0/0
    newCassandra2.writelines(str(int(time.mktime(datetime.datetime.strptime(formatTimestamp(temp), "%d/%m/%Y %H:%M:%S").timetuple()))))
newCassandra2.close()
>>>>>>> develop:psd/projeto/limpeza_dados/clear_data.py
