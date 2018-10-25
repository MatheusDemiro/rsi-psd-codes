import datetime
import time

def formatTimestamp(array):
    hour = str(int(array[1][0:2])-3)
    string = array[0]+" "+hour+array[1][2:]

    return string

cassandra2 = open("Cassandra2.TXT","r+")
newCassandra2 = open("newCassandra2.txt","w+")

data = cassandra2.readlines()

cassandra2.close()

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
