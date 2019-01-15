import pickle as p

class CreateWindow:
    def __init__(self, COLLECTION_PATH, WINDOW_SIZE, UNIQUE_MACS_PATH):
        self.COLLECTION_PATH = COLLECTION_PATH
        self.WINDOW_SIZE = WINDOW_SIZE
        self.UNIQUE_MACS_PATH = UNIQUE_MACS_PATH
        self.UNIQUE_MACS = []

    #Metodo que retorna as informacoes da primeira linha do arquivo para servir como referencia ao andamenta da limpeza dos dados
    def header(self, data):
        first = data.pop(0)[:-1].split(",")
        RSSI = int(first[0])
        TS = int(first[2])
        MAC = first[1]
        dic = {MAC: ([int(RSSI)], 1)}

        return dic, MAC, TS

    # Metodo que retorna o array com todas as janelas de tempo
    def openFile(self):
        arq = open(self.COLLECTION_PATH, "rb")
        temp = p.load(arq)
        arq.close()
        return temp

    #Metodo que salva os MACS unicos
    def saveUniqueMacs(self): #Filtrar pelo valor da frequência
        arq = open(self.UNIQUE_MACS_PATH, "wb")
        p.dump(self.UNIQUE_MACS, arq)
        arq.close()
        return self.UNIQUE_MACS

    def fillUniqueMacs(self, data):
        for mac in data:
            if mac not in self.UNIQUE_MACS:
                    self.UNIQUE_MACS.append(mac)
        return self.UNIQUE_MACS

    #Metodo que calcula a media do RSSI de cada tupla ([RSSI],freq)
    def average(self, dic):
        for i in dic:
            temp = dic[i]
            dic[i] = (round(sum(temp[0]) / temp[1], 2), temp[1])
        return dic

    #Metodo que executa filtra os dados em janelas de tempo
    def execution(self):
        data = self.openFile()  # Abrindo arquivo com as coletas
        dic, currentMAC, windowTS = self.header(data)  # Salvando informacoes da primeira linha do arquivo
        # Intel Corporate (PC LAB) = 84-34-97/60-67-20(wi-fi)
        windows = []
        for i in data:
            RSSI, MAC, TS = i[:-1].split(",")
            currentMAC = MAC
            if (int(TS) - windowTS) < self.WINDOW_SIZE:
                if currentMAC in dic:
                    temp = dic[currentMAC]
                    temp[0].append(int(RSSI))
                    dic[currentMAC] = (temp[0], temp[1] + 1)
                else:
                    dic[currentMAC] = ([int(RSSI)], 1)
            else:
                windows.append(self.average(dic))
                self.fillUniqueMacs(dic)
                windowTS = int(TS)
                dic = {MAC: ([int(RSSI)], 1)}  # Preparando dicionario para a proxima janela
        self.saveUniqueMacs()
        return windows