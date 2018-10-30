import csv
import datetime
import time

def formatDate(array):
    hour = array[1][0:2]
    if hour == "00":
        if array[0][3:5] == '01':
            aux = array[0].split()
            aux1 = aux[0].split("/")
            aux1[0] = '10'
            aux1[1] = '31'
            aux[0] = "/".join(aux1)
            array[0] = " ".join(aux)
        else:
            array[0] = array[0].replace(array[0][3:5], str(int(array[0][3:5])-1))
    elif hour == "01":
        time = "22"
        if array[0][3:5] == '01':
            aux = array[0].split()
            aux1 = aux[0].split("/")
            aux1[0] = '10'
            aux1[1] = '31'
            aux[0] = "/".join(aux1)
            array[0] = " ".join(aux)
        else:
            array[0] = array[0].replace(array[0][3:5], str(int(array[0][3:5])-1))
    elif hour == "02":
        time = "23"
        if array[0][3:5] == '01':
            aux = array[0].split()
            aux1 = aux[0].split("/")
            aux1[0] = '10'
            aux1[1] = '31'
            aux[0] = "/".join(aux1)
            array[0] = " ".join(aux)
        else:
            array[0] = array[0].replace(array[0][3:5], str(int(array[0][3:5])-1))
    else:
        time = str(int(hour))
    date = array[0].split("/")
    date[2] = "2016"
    return "/".join(date)+" "+time+array[1][2:]

novaTabela = open("arquivos/pasto2.csv", "w", newline='') #Arquivo aberto no modo de escrita
tabela = open("pasto.csv","r") #Arquivo aberto no modo de leitura

try:
    dados = csv.reader(tabela)
    gravar = csv.writer(novaTabela, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    gravar.writerow(['timestamp_abrigo','tbs','ur','tgn','tpo']) #Rotulos das colunas
    c=0 #Variavel que serve para sinalizar ao algoritmo sobre os rotulos das colunas
    for linha in dados:
        temp = linha[0].split(";")
        if c >= 1 and temp[0] != "":
            temp[0] = temp[0].replace("h",":").replace("min",":").replace("s","")
            timestamp = str(int(time.mktime(datetime.datetime.strptime(formatDate(temp[0].split()), "%m/%d/%Y %H:%M:%S").timetuple())))
            temp[0] = timestamp
            if temp[3] == '':
                temp[3] = "-"
            gravar.writerow(temp)
        c+=1
finally:
    tabela.close()
    novaTabela.close()
    
'''
#Reverse engineering

from datetime import datetime

a = open("arquivos/newCassandra2.txt","r")

b = a.readlines()

a.close()

for i in b:
    print(datetime.utcfromtimestamp(int(i[0:-1])).strftime('%m/%d/%Y %H:%M:%S'))
'''