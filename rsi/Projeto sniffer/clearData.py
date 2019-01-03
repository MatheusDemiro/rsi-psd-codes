import pickle as p
import os

#Metodo que abre o arquivo para limpeza
def openFile(path):
    arq = open(path,"r+")
    data = arq.readlines()
    arq.close()

    return data

#Metodo que salva as listas com os dados limpos
def saveWindows(windows):
    arq = open("WINDOWS.pickle", "wb")
    p.dump(windows, arq)
    arq.close()

#Metodo que retorna as informacoes da primeira linha do arquivo para servir como referencia ao andamenta da limpeza dos dados
def header(data):
    first = data.pop(0)[:-1].split(",")
    RSSI = int(first[0])
    TS = int(first[2])
    MAC = first[1]
    dic = {MAC:([int(RSSI)],1)}

    return dic, MAC, TS

#Metodo que retorna True para os encerecos MACs validos e False para os nao validos
def validateMAC(MAC):
    global allIntelCorporateMAC

    mac = MAC.split(":")
    result = "0x"+mac[0]
    if int(result, 16) & 2 == 2: #MAC local
        return False
    else: #MAC universal
        if ":".join(mac[:3]) == "60:67:20": #Nao for do fornecedor "Intel Corporate"
            if MAC not in allIntelCorporateMAC:
                allIntelCorporateMAC.append(MAC)
            return False
        return True

#Metodo que calcula a media do RSSI de cada tupla ([RSSI],freq)
def average(dic):
     for i in dic:
         temp = dic[i]
         dic[i] = (sum(temp[0])/temp[1], temp[1])
     return dic

data = openFile(os.getcwd()+"\\COLETA_PBD_21-12-18.txt") #Abrindo arquivo com as coletas
dic,currentMAC, windowTS = header(data) #Salvando informacoes da primeira linha do arquivo
currentTS = windowTS
#Intel Corporate (PC LAB) = 84-34-97/60-67-20(wi-fi)

windows = []
for i in data:
    RSSI,MAC,TS = i[:-1].split(",")
    currentMAC = MAC
    if (int(TS) - windowTS) < 120:
        if currentMAC in dic:
            temp = dic[currentMAC]
            temp[0].append(int(RSSI))
            dic[currentMAC] = (temp[0], temp[1] + 1)
        else:
            dic[currentMAC] = ([int(RSSI)], 1)
        currentTS = int(TS)
    else:
        windows.append(average(dic))
        windowTS = int(TS)
        dic = {MAC: ([int(RSSI)], 1)} #Preparando dicionario para a proxima janela
        currentTS = int(TS)

saveWindows(windows) #Salvando janela

#Para deteccoes com media de RSSI maior que 85 obtemos um totalRepetitions de 42 pacotes capturados, sendo que apenas 32 (16 pessoas e 16 maquinas)
#correspondem a realidade da sala de aula (observacao).
#Para a primeira janela de tempo admiti uma quantidade de aparicoes de 20 vezes com media de RSSI maior que 50, sendo coletados exatamente
#32 pacotes, que por mera coincidencia correspondem as 16 pessoas e 16 maquinas presentes em sala.

     ##############################################################################################################
###### OBS.: OS ENDERECOS MACs NAO POSSUEM REPETICAO NA JANELA, POREM PODEM APARECER MAIS DE UMA VEZ EM JANELAS DISTINTAS ######
     ##############################################################################################################
