from algorithms.CreateWindow import CreateWindow
from data.Baseline import Baseline
from algorithms.ClearData import ClearData
import pickle as p

WINDOW_SIZE = 300 #5 minutos
COLLECTION_PATH = "data\\COLETA_PBD_13-12-18.txt"
CLEAR_COLLECTION_PATH = "data_structure\\(CLEAR)"+COLLECTION_PATH.split("\\")[1][:-4]
BASELINE_PATH = "data_structure\\BASELINE.pickle"
UNIQUE_MACS_BEF_PATH = "data_structure\\(BF)UNIQUE_MACS_PBD_13-12-18" #Antes
UNIQUE_MACS_AFT_PATH = "data_structure\\(AF)UNIQUE_MACS_PBD_13-12-18" #Depois

FREQUENCY = 30
AVERAGE_RSSI = -70

def openFile(PATH):
    arq = open(PATH, "rb")
    temp = p.load(arq)
    arq.close()
    return temp

#Se o arquivo de execucao for o modulo principal
if __name__ == "__main__":
    #Criando instancias e chamando os respectivos metodos de execucao
    clearData = ClearData(COLLECTION_PATH, CLEAR_COLLECTION_PATH, UNIQUE_MACS_BEF_PATH)
    clearData.execution()

    baseline_instance = Baseline(CLEAR_COLLECTION_PATH, BASELINE_PATH, WINDOW_SIZE, FREQUENCY, AVERAGE_RSSI)
    createWindow = CreateWindow(CLEAR_COLLECTION_PATH, WINDOW_SIZE, UNIQUE_MACS_AFT_PATH)
    #print(createWindow.execution())
    baseline = baseline_instance.generateClassifier(createWindow.execution())
    baseline_instance.saveWindows(baseline)
    print("\nENDEREÇOS MACS E SEUS RESULTADOS POR JANELA")
    for i in baseline:
        print(i,baseline[i])
    print("\nQuantidade total de macs:", len(baseline))
    print("\nQuantidade de MACs antes da limpeza:", len(openFile(UNIQUE_MACS_BEF_PATH)))
    print("Quantidade de MACs após a limpeza:", len(openFile(UNIQUE_MACS_AFT_PATH)))
