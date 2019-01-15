import pickle as p
from itertools import zip_longest

class Classifier:
    def __init__(self, BASELINE_PATH, WINDOWS):
        self.BASELINE_PATH = BASELINE_PATH
        #self.AVERAGE_RSSI = AVERAGE_RSSI
        #self.AVERAGE_FREQ = AVERAGE_FREQ
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
                if mac in self.WINDOWS[index] and mac in self.WINDOWS[index+1]:
                        if mac not in classifier:
                            classifier[mac] = [0]*length
                            classifier[mac][index] = 1
                            classifier[mac][index+1] = 1
                        else:
                            classifier[mac][index] = 1
                            classifier[mac][index+1] = 1
                else:
                    if mac not in classifier:
                        classifier[mac] = [0] * length
        print(classifier["e0:9d:31:74:d0:44"])
        return classifier

    #Metodo que verifica se o grupo tem 1's sequenciais
    def verifyGrouping(self, data):
        for i in range(len(data) - 1):
            if data[i] == 1 and data[i + 1] == 1:
                return True
        return False

    #Metodo que agrupa os dados da lista teste baseado na diferenca de tamannho dos dados da baseline
    def grouping(self, comparation, group):
        for mac in comparation:
            args = [iter(comparation[mac])] * group
            temp = list(zip_longest(*args, fillvalue=None))
            for value in range(len(temp)): #Verificar se tem 1's sequenciais
                if self.verifyGrouping(temp[value]):
                    temp[value] = 1
                else:
                    temp[value] = 0
            comparation[mac] = temp
        return comparation

    #Metodo que os macs incompatíveis
    def printError(self, baseline, comparation):
        print("\nMACS QUE NÃO APARECERAM EM JANELAS SEQUENCIAIS\n")
        totalErrors = 1
        for mac in baseline:
            if mac not in comparation:
                print("MAC %d: %s" % (totalErrors, mac))
                totalErrors += 1

    #Metodo que exibe os erros
    def printErrorRates(self, baseline, comparation):
        print("\nTAXAS DE ERRO\n")
        lengthB = len(baseline[list(baseline.keys())[0]])
        lengthC = len(comparation[list(comparation.keys())[0]])
        group = lengthC // lengthB
        comparation = self.grouping(comparation, group)
        totalErrors, average = 0, 0  # Quantidade total e media dos erros, respectivamente
        countMac = 1
        for mac in comparation:
            errorsMAC = 0  # Quantidade de erros por mac
            value = comparation[mac]
            if mac in baseline:
                value2 = baseline[mac]
                for i in range(lengthB):
                    # if mac == "50:92:b9:91:20:2e":
                    #     print(value, value2)
                    if value[i] != value2[i]:
                        errorsMAC += 1
                        totalErrors += 1
            percentage = (errorsMAC * 100) / lengthB  # Ou len(comparation[mac]), mas este possui um dado a mais que o baseline[mac]
            print("MAC ADDRESS %d: %s. Error: %.2f%%" % (countMac, mac, percentage))
            average += percentage
            countMac += 1
        print("\nERROR AVERAGE: %.2f%%" %(average/len(comparation)))
        print("SUCESS AVERAGE: %.2f%%" %(100-(average/len(comparation))))
        self.printError(baseline, comparation)

    #Metodo que executa as funcionalidadse da classe
    def execution(self):
        baseline = self.openBaseline()
        comparation = self.comparationBaseline(baseline)
        self.printErrorRates(baseline, comparation)
        return comparation