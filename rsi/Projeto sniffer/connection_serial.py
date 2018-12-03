import serial
import time

#[RSSI,MAC]

def header(data):
    first = setTimestamp(data).split(",")
    RSSI = first[0]
    TS = int(first[2])
    MAC = first[1]
    dic = {MAC:([int(RSSI)],1)}

    return dic, MAC, TS

def setTimestamp(data):
    return data.decode()[:-2]+","+str(int(time.time()))

def average(dic):
    for i in dic:
        temp = dic[i]
        dic[i] = (sum(temp[0])/temp[1], temp[1])
    return dic

comport = serial.Serial('com10', 115200)
arq = open("data_sniffer.txt", "w+")

dic, MAC, windowTS = header(comport.readline())
currentTS = windowTS
windows = [] #Lista com todos os dados coletados durante a janela
while True:
    data = setTimestamp(comport.readline())
    if not data:
        break
    RSSI, MAC, TS = data[:-1].split(",")
    if currentTS != int(TS):
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
    print(dic)
    arq.writelines(data+"\n")
arq.close()
comport.close()
print(windows)