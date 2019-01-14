from data.Baseline import Baseline
from algorithms.ClearData import ClearData

WINDOW_SIZE = 300 #5 minutos
COLLECTION_PATH = "data\\COLETA_PBD_13-12-18.txt"
CLEAR_COLLECTION_PATH = "data_structure\\(CLEAR)"+COLLECTION_PATH.split("\\")[1][:-4]
BASELINE_PATH = "data_structure\\BASELINE.pickle"

AVERAGE_FREQ = 18
AVERAGE_RSSI = -80

#Se o arquivo de execucao for o modulo principal
if __name__ == "__main__":
    #Criando instancias e chamando os respectivos metodos de execucao
    clearData = ClearData(COLLECTION_PATH, CLEAR_COLLECTION_PATH)
    clearData.execution()

    baseline = Baseline(CLEAR_COLLECTION_PATH, BASELINE_PATH, WINDOW_SIZE, AVERAGE_FREQ, AVERAGE_RSSI)
    exe = baseline.execution()
    for i in exe:
        print(i,exe[i])
    print(len(exe))        
