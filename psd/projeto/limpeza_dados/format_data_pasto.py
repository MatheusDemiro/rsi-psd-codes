import csv

dic = {"01":"13","02":"14","03":"15","04":"16","05":"17","06":"18","07":"19","08":"20","09":"21","10":"22","11":"23","12":"00"}

def formatDate(array): #Parametros: [<data/hora>,<turno>]
    date = array[0].split("/")
    date[2] = "2016"
    hour = array[0].split()[1].split(":")  # time = str(int(hour))
    if array[1] == "N" and hour[0] != "12":
        hour[0] = dic[hour[0]] #Substituindo hora
    elif array[1] == "D" and hour[0] == "12":
        hour[0] = dic[hour[0]]
    return "/".join(date)+" "+":".join(hour)

novaTabela = open("arquivos/fomart_pasto.csv", "w", newline='') #Arquivo aberto no modo de escrita
tabela = open("arquivos/pasto_zero.csv","r") #Arquivo aberto no modo de leitura

try:
    dados = csv.reader(tabela)
    gravar = csv.writer(novaTabela, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    columns = next(dados)[0].split(";")
    columns.remove("turno") #removendo coluna turno
    gravar.writerow(columns) #Rotulos das colunas
    for linha in dados:
        temp = linha[0].split(";")
        if temp[0] != "":
            temp[0] = temp[0].replace("h",":").replace("min",":").replace("s","")
            temp[0] = formatDate(temp[0:2])
            if temp[3] == '':
                temp[3] = "-"
            del temp[1]
            gravar.writerow(temp)
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