import pickle as p

class CollectData:
    def __init__(self, PATH):
        self.PATH = PATH

    #Metodo que abre o arquivo para limpeza
    def openFile(self):
        arq = open(self.PATH,"r+")
        data = arq.readlines()
        arq.close()

        return data

    #Metodo que salva as listas com os dados limpos
    def saveWindows(self, windows):
        arq = open("Data structure\\WINDOWS.pickle", "wb")
        p.dump(windows, arq)
        arq.close()

    #Metodo que retorna as informacoes da primeira linha do arquivo para servir como referencia ao andamenta da limpeza dos dados
    def header(self, data):
        first = data.pop(0)[:-1].split(",")
        RSSI = int(first[0])
        TS = int(first[2])
        MAC = first[1]
        dic = {MAC:([int(RSSI)],1)}

        return dic, MAC, TS

    #Metodo que calcula a media do RSSI de cada tupla ([RSSI],freq)
    def average(self, dic):
         for i in dic:
             temp = dic[i]
             dic[i] = (sum(temp[0])/temp[1], temp[1])
         return dic

    #Metodo que executa filtra os dados em janelas de tempo
    def execution(self):
        data = self.openFile() #Abrindo arquivo com as coletas
        dic,currentMAC, windowTS = self.header(data) #Salvando informacoes da primeira linha do arquivo
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
            else:
                windows.append(self.average(dic))
                windowTS = int(TS)
                dic = {MAC: ([int(RSSI)], 1)} #Preparando dicionario para a proxima janela
        self.saveWindows(windows) #Salvando janela

#Para deteccoes com media de RSSI maior que 85 obtemos um totalRepetitions de 42 pacotes capturados, sendo que apenas 32 (16 pessoas e 16 maquinas)
#correspondem a realidade da sala de aula (observacao).
#Para a primeira janela de tempo admiti uma quantidade de aparicoes de 20 vezes com media de RSSI maior que 50, sendo coletados exatamente
#32 pacotes, que por mera coincidencia correspondem as 16 pessoas e 16 maquinas presentes em sala.

     ##############################################################################################################
###### OBS.: OS ENDERECOS MACs NAO POSSUEM REPETICAO NA JANELA, POREM PODEM APARECER MAIS DE UMA VEZ EM JANELAS DISTINTAS ######
     ##############################################################################################################
