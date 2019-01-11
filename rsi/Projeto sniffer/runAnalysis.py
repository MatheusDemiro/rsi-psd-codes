from data.baseline import Baseline
from algorithms.clearData import ClearData

WINDOW_SIZE = 300 #5 minutos
COLLECTION_PATH = "data\\COLETA_PBD_13-12-18.txt"
BASELINE_PATH = "data structure\\BASELINE.pickle"

#Se o arquivo de execucao for o modulo principal
if __name__ == "__main__":
    #Criando instancias
    baseline = Baseline(COLLECTION_PATH, BASELINE_PATH, WINDOW_SIZE)
    clearData = ClearData(BASELINE_PATH)

    #Chamando metodos de execucao
    baseline.execution()
    clearData.execution()
