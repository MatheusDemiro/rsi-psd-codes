import pickle as p

from algorithms.CreateWindow import CreateWindow


class Baseline:
    def __init__(self, COLLECTION_PATH, BASELINE_PATH, WINDOW_SIZE, AVERAGE_FREQ, AVERAGE_RSSI):
        self.COLLECTION_PATH = COLLECTION_PATH
        self.WINDOW_SIZE = WINDOW_SIZE
        self.BASELINE_PATH = BASELINE_PATH
        self.AVERAGE_FREQ = AVERAGE_FREQ
        self.AVERAGE_RSSI = AVERAGE_RSSI

    #Metodo que abre a colecao de dados
    def openFile(self):
        arq = open(self.COLLECTION_PATH, "rb")
        temp = p.load(arq)
        arq.close()
        return temp

    # #Metodo que salva os MACS unicos
    # def saveUniqueMacs(self): #Filtrar pelo valor da frequência
    #     arq = open("data_structure\\UNIQUE_MACS", "wb")
    #     p.dump(self.UNIQUE_MACS, arq)
    #     arq.close()
    #     return self.UNIQUE_MACS

    # def fillUniqueMacs(self, data):
    #     print(data)
    #     for mac in data:
    #         if mac not in self.UNIQUE_MACS and data[mac][0] <= self.AVERAGE_RSSI:
    #             if data[mac][1] >= self.AVERAGE_FREQ:
    #                 print(mac)
    #                 self.UNIQUE_MACS.append(mac)
    #     return self.UNIQUE_MACS

    #Metodo que salva as janelas limpas
    def saveWindows(self, baseline):
        arq = open(self.BASELINE_PATH, "wb")
        p.dump(baseline, arq)
        arq.close()
        return baseline

    #Metodo que gera a classificacao dos MACs (ocupante e nao ocupante)
    def generateClassifier(self, windows):
        baseline = {}
        length = len(windows)
        for index in range(length-1):
            for mac in windows[index]:
                timeWindow = windows[index]
                if mac in windows[index+1] and timeWindow[mac][0] <= self.AVERAGE_RSSI:
                    if timeWindow[mac][1] >= self.AVERAGE_FREQ:
                        if mac not in baseline:
                            baseline[mac] = [0]*length
                            baseline[mac][index] = 1
                            baseline[mac][index+1] = 1
                        else:
                            baseline[mac][index] = 1
                            baseline[mac][index+1] = 1
        return baseline

    #Metodo que executa as funcionalidadse da classe
    def execution(self):
        createWindow = CreateWindow(self.COLLECTION_PATH, self.WINDOW_SIZE)
        baseline = self.generateClassifier(createWindow.execution())
        self.saveWindows(baseline)
        return baseline
