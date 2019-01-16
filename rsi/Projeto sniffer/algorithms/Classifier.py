import pickle as p
from itertools import zip_longest

class Classifier:
    def __init__(self, BASELINE_PATH, WINDOWS, FREQUENCY, AVERAGE_RSSI):
        self.BASELINE_PATH = BASELINE_PATH
        self.WINDOWS = WINDOWS
        self.FREQUENCY = FREQUENCY
        self.AVERAGE_RSSI = AVERAGE_RSSI

    #Metodo que abre o baseline
    def openBaseline(self):
        arq = open(self.BASELINE_PATH, "rb")
        temp = p.load(arq)
        arq.close()
        return temp

    #Metodo que compara os dados testes com o baseline
    def classifierMacs(self, baseline):
        classifier = {}
        length = len(self.WINDOWS)
        for mac in baseline:
            for index in range(length-1):
                if mac in self.WINDOWS[index] and mac in self.WINDOWS[index+1]:#Janelas consecutivas
                    window = self.WINDOWS[index]
                    if window[mac][1] >= self.FREQUENCY and window[mac][0] <= self.AVERAGE_RSSI:
                        if mac not in classifier:
                            classifier[mac] = [0]*length
                            classifier[mac][index] = 1
                            classifier[mac][index+1] = 1
                        else:
                            classifier[mac][index] = 1
                            classifier[mac][index+1] = 1
        return classifier

    #Metodo que verifica se o grupo tem 1's sequenciais
    def verifyGrouping(self, data):
        for i in range(len(data) - 1):
            if data[i] == 1 and data[i + 1] == 1:
                return True
        return False

    #Metodo que elimina as aparaicoes nao consecutivas
    def clearGroup(self, data):
        for i in range(len(data)):
            aux = list(data[i])
            if aux[0] == 1 and aux[1] == 0:
                aux[0] = 0
            if aux[-1] == 1 and aux[-2] == 0:
                aux[-1] = 0
            for j in range(len(data[i]) - 1):
                if aux[j] == 1 and aux[j - 1] == 0 and aux[j + 1] == 0:
                    aux[j] = 0
            data[i] = aux
        return data

    #Metodo que agrupa os dados da lista teste baseado na diferenca de tamannho dos dados da baseline
    def grouping(self, comparation, group):
        for mac in comparation:
            args = [iter(comparation[mac])] * group
            temp = self.clearGroup(list(zip_longest(*args, fillvalue=None)))
            comparation[mac] = temp
        return comparation

    #Metodo que os macs incompatíveis
    def printError(self, baseline, comparation):
        print("\nMACS QUE NÃO APARECERAM EM JANELAS CONSECUTIVAS\n")
        totalErrors = 1
        for mac in baseline:
            if mac not in comparation:
                print("MAC %d: %s" % (totalErrors, mac))
                totalErrors += 1

    #Metodo que exibe os erros
    def comparationBaseline(self, baseline, comparation):
        print("\nTAXAS DE ERRO\n")
        lengthB, lengthC = len(baseline[list(baseline.keys())[0]]), len(comparation[list(comparation.keys())[0]])
        group = int(round(lengthC / lengthB, 0))
        comparation = self.grouping(comparation, group)
        average, countMac, length = 0, 1, min(lengthC//group, lengthB)
        for mac in comparation:
            errorsMAC = 0  # Quantidade de erros por mac
            if mac in baseline:
                for index in range(length): #Calcular erro para cada mac do dicionario comparation
                    if baseline[mac][index] == 1:
                        errorsMAC += comparation[mac][index].count(0)
                    else:
                        errorsMAC += comparation[mac][index].count(1)
            percentage = (errorsMAC * 100) / lengthC  # Ou len(comparation[mac]), mas este possui um dado a mais que o baseline[mac]
            print("MAC ADDRESS %d: %s. Error: %.2f%%" % (countMac, mac, percentage))
            average += percentage
            countMac += 1
        print("\nERROR AVERAGE: %.2f%%" %(average/len(comparation)))
        print("SUCESS AVERAGE: %.2f%%" %(100-(average/len(comparation))))
        if countMac-1 != len(baseline):
            self.printError(baseline, comparation)

    #Metodo que executa as funcionalidadse da classe
    def execution(self):
        baseline = self.openBaseline()
        comparation = self.classifierMacs(baseline)
        self.comparationBaseline(baseline, comparation)
        return comparation