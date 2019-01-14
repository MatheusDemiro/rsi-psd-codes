import pickle as p
from itertools import zip_longest

class Classifier:
    def __init__(self, BASELINE_PATH, AVERAGE_RSSI, AVERAGE_FREQ, WINDOWS):
        self.BASELINE_PATH = BASELINE_PATH
        self.AVERAGE_RSSI = AVERAGE_RSSI
        self.AVERAGE_FREQ = AVERAGE_FREQ
        self.WINDOWS = WINDOWS

    #Metodo que abre o baseline
    def openBaseline(self):
        arq = open(self.BASELINE_PATH, "rb")
        temp = p.load(arq)
        arq.close()
        return temp

    #Metodo que compara os dados testes com o baseline
    def comparationBaseline(self, baseline):
        classifier = {}
        length = len(self.WINDOWS)
        for mac in baseline:
            for index in range(length-1):
                timeWindow = self.WINDOWS[index]
                if mac in self.WINDOWS[index] and mac in self.WINDOWS[index+1]:
                    if timeWindow[mac][1] >= self.AVERAGE_FREQ and timeWindow[mac][0] <= self.AVERAGE_RSSI:
                        if mac not in classifier:
                            classifier[mac] = [0]*length
                            classifier[mac][index] = 1
                            classifier[mac][index+1] = 1
                        else:
                            classifier[mac][index] = 1
                            classifier[mac][index+1] = 1
        return classifier

    #Metodo que agrupa os dados da lista teste baseado na diferenca de tamannho dos dados da baseline
    def grouping(self, comparation, group):
        for mac in comparation:
            args = [iter(comparation[mac])] * group
            temp = list(zip_longest(*args, fillvalue=None))
            for value in range(len(temp)): #len(temp) = int(round(lengthC/group),0)
                if 1 in temp[value]:
                    temp[value] = 1
                else:
                    temp[value] = 0
            comparation[mac] = temp
        return comparation

    #Metodo que exibe os erros
    #(PROBLEMA: comparation e baseline apresentam tamanhos de listas distintas mesmo apos o agrupamento).
    #Para 1 minuto a tabela comparation fica com 13 janelas, enquanto o baseline tem 12 para 5 minutos.
    def printError(self, baseline, comparation):
        print("\nMACS CLASSIFICADOS COMO NÃO OCUPANTES\n")
        totalErrors = 1
        for mac in baseline:
            if mac not in comparation:
                print("MAC %d: %s" %(totalErrors,mac))
                totalErrors+=1
        print("\nTAXAS DE ERRO\n")
        lengthB = len(baseline[list(baseline.keys())[0]])
        lengthC = len(comparation[list(comparation.keys())[0]])
        group = lengthC//lengthB
        comparation = self.grouping(comparation, group)
        totalErrors, average = 0, 0 #Quantidade total e media dos erros, respectivamente
        for mac in baseline:
            errorsMAC = 0 #Quantidade de erros por mac
            value = baseline[mac]
            if mac in comparation:
                value2 = comparation[mac]
                for i in range(lengthB):
                    # if mac == "50:92:b9:91:20:2e":
                    #     print(value, value2)
                    if value[i] != value2[i]:
                        errorsMAC += 1
                        totalErrors += 1
            percentage = (errorsMAC * 100) / lengthB #Ou len(comparation[mac]), mas este possui um dado a mais que o baseline[mac]
            print("MAC ADDRESS %d: %s. Error: %.2f%%" % (totalErrors, mac, percentage))
            average += percentage
        print("\nAVERAGE: %.2f%%" % (average / totalErrors))
        # average, count = 0,1
        # for mac in comparation:
        #     percentage = (comparation[mac].count(0) * 100) / len(comparation[mac])
        #     print("MAC ADDRESS %d: %s. Error: %.2f" % (count, mac, percentage))
        #     average += percentage
        #     count+=1
        # print("\nAVERAGE: %.2f" % (average / count))
        # print(comparation)

    #Metodo que executa as funcionalidadse da classe
    def execution(self):
        baseline = self.openBaseline()
        comparation = self.comparationBaseline(baseline)
        self.printError(baseline, comparation)
        return comparation