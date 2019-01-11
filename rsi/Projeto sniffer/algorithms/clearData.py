import pickle as p

class ClearData:
    def __init__(self, WINDOW_PATH):
        self.WINDOW_PATH = WINDOW_PATH
        self.fakeMACWindow = []
        self.intelCorporateMACWindow = []

    #Metodo que retorna a lista com as janelas de captura limpas
    def clearMAC(self, windows):
        count = 0
        clearWindows = []
        while count < len(windows):
            auxFake, auxWindow, auxIntel = [], {}, []
            for MAC in windows[count]:
                mac = MAC.split(":")
                result = "0x" + mac[0]
                if int(result, 16) & 2 == 2:  #MAC local (falso)
                    auxFake.append(MAC)
                    continue
                else:  #MAC universal
                    if ":".join(mac[:3]) == "60:67:20":  #Se for do fornecedor "Intel Corporate"
                        if MAC not in auxIntel:
                            auxIntel.append(MAC)
                            continue
                auxWindow[MAC] = windows[count][MAC]
            count+=1
            if auxFake == []:
                auxFake.append(0)
            elif auxIntel == []:
                auxIntel.append(0)
            self.fakeMACWindow.append(auxFake);clearWindows.append(auxWindow);self.intelCorporateMACWindow.append(auxIntel)
        return clearWindows

    #Metodo que salva as janelas limpas
    def saveWindows(self, windows):
        arq = open(self.WINDOW_PATH, "wb")
        p.dump(windows, arq)
        arq.close()

        return windows

    #Metodo que retorna o array com todas as janelas de tempo
    def openWindows(self):
        arq = open(self.WINDOW_PATH, "rb")
        temp = p.load(arq)
        arq.close()
        return temp

    #Metodo que executa o algoritmo de limpeza
    def execution(self):
        windows = self.openWindows()
        return self.saveWindows(self.clearMAC(windows))