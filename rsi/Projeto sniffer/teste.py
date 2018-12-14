def openFile(path):
    arq = open(path,"r+")
    data = arq.readlines()
    arq.close()

    return data

def header(data):
    first = data.pop(0)[:-1].split(",")
    RSSI = int(first[0])
    TS = int(first[2])
    MAC = first[1]
    dic = {MAC:([int(RSSI)],1)}

    return dic, MAC, TS

def average(dic):
     for i in dic:
         temp = dic[i]
         dic[i] = (sum(temp[0])/temp[1], temp[1])
     return dic

data = openFile("C:\\Users\\User\\Documents\\GitKraken\\rsi-psd-codes\\rsi\\Projeto sniffer\\COLETA_PBD_13-12-18.txt")
dic,currentMAC, windowTS = header(data)
currentTS = windowTS
windows = [] #Lista com todos os dados coletados durante a janela
for i in data:
    RSSI,MAC,TS = i[:-1].split(",")
    print(currentTS, currentMAC)
    currentMAC = MAC
    if (int(TS) - windowTS) < 300:
        if currentMAC in dic:
            temp = dic[currentMAC]
            temp[0].append(int(RSSI))
            dic[currentMAC] = (temp[0], temp[1] + 1)
        else:
            dic[currentMAC] = ([int(RSSI)], 1)
        currentTS = int(TS)
    else:  # 5 minutes (time-window)
        windows.append(average(dic))
        windowTS = int(TS)
        dic = {MAC: ([int(RSSI)], 1)}
        currentTS = int(TS)
print(len(windows))
print(windows)

#Para detecções com média de RSSI maior que 85 obtemos um total de 42 pacotes capturados, sendo que apenas 32 (16 pessoas e 16 máquinas)
#correspondem a realidade da sala de aula (observação).
#Para a primeira janela de tempo admiti uma quantidade de aparições de 20 vezes com média de RSSI maior que 50, sendo coletados exatamente
#32 pacotes, que por mera coincidência correspondem as 16 pessoas e 16 máquinas presentes em sala.