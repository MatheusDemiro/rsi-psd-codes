import pickle as p
import codecs

class ClearData:
    def __init__(self, COLLECTION_PATH, CLEAR_COLLECTION_PATH):
        self.COLLECTION_PATH = COLLECTION_PATH
        self.CLEAR_COLLECTION_PATH = CLEAR_COLLECTION_PATH
        self.fakeMACWindow = []
        self.intelCorporateMACWindow = []

    #Metodo que retorna a lista com as janelas de captura limpas
    def clearMAC(self, data):
        clearFile = []
        auxFake, auxIntel = [], []
        for MAC in data:
            mac = MAC.split(",")[1].split(":")
            result = "0x" + mac[0]
            if int(result, 16) & 2 == 2:  #MAC local (falso)
                auxFake.append(MAC)
                continue
            else:  #MAC universal
                if ":".join(mac[:3]) == "60:67:20":  #Se for do fornecedor "Intel Corporate"
                    if MAC not in auxIntel:
                        auxIntel.append(MAC)
                        continue
            clearFile.append(MAC)
        return clearFile

    #Metodo que salva as janelas limpas
    def saveWindows(self, data):
        arq = open(self.CLEAR_COLLECTION_PATH, "wb")
        p.dump(data, arq)
        arq.close()
        return data

    #Metodo que retorna o array com todas as janelas de tempo
    def openFile(self):
        arq = codecs.open(self.COLLECTION_PATH, "rb", encoding='utf-8')
        temp = arq.readlines()
        arq.close()
        return temp

    #Metodo que executa o algoritmo de limpeza
    def execution(self):
        data = self.openFile()
        return self.saveWindows(self.clearMAC(data))