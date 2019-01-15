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
