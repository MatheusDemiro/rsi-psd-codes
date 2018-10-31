import csv
import datetime
import time

novaTabela = open("arquivos/pasto2.csv", "w", newline='')  # Arquivo aberto no modo de escrita
tabela = open("arquivos/fomart_pasto.csv", "r")  # Arquivo aberto no modo de leitura

try:
    dados = csv.reader(tabela)
    next(dados) #Pulando os rotulos das colunas
    gravar = csv.writer(novaTabela, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    gravar.writerow(['timestamp_abrigo', 'tbs', 'ur', 'tgn', 'tpo'])  # Rotulos das colunas
    for linha in dados:
        temp = linha[0].split(";")
        if temp[0] != "":
            temp[0] = temp[0].replace("h", ":").replace("min", ":").replace("s", "") #Trocando os elementos inconsistentes
            timestamp = str(int(time.mktime(datetime.datetime.strptime(temp[0], "%m/%d/%Y %H:%M:%S").timetuple())))
            temp[0] = timestamp
            if temp[3] == '':
                temp[3] = "-"
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