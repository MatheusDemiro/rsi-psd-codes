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
    dic = {MAC:(int(RSSI),1)}

    return dic, MAC, TS

data = openFile("C:\\Users\\User\\Documents\\GitKraken\\rsi-psd-codes\\rsi\\Projeto sniffer\\data_sniffer.txt")
dic,currentMAC, windowTS = header(data)
currentTS = windowTS
windows = [] #Lista com todos os dados coletados durante a janela
for i in data:
    RSSI,MAC,TS = i[:-1].split(",")
    if currentTS != int(TS):
        currentMAC = MAC
        if (int(TS) - windowTS) < 300:
            if currentMAC in dic:
                temp = dic[currentMAC]
                if temp[1] > 1:
                    dic[currentMAC] = (temp[0]+(int(RSSI)/2),temp[1]+1)
                else:
                    dic[currentMAC] = ((temp[0]+int(RSSI))/2,temp[1]+1)
            else:
                dic[currentMAC] = (int(RSSI),1)
            currentTS = int(TS)
        else: #5 minutes (time-window)
            windows.append(dic)
            windowTS = int(TS)
            dic = {MAC:(int(RSSI),1)}
            currentTS = int(TS)
    print(dic)
