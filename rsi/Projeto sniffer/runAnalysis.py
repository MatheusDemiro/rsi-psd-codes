from data.baseline import Baseline
from algorithms.clearData import ClearData
import os

WINDOW_SIZE = 120
COLLECTTION_PATH = os.getcwd() +"\\data\\COLETA_PBD_21-12-18.txt"

BASELINE_PATH = "data structure\\BASELINE.pickle"

#Se o arquivo de execucao for o modulo principal
if __name__ == "__main__":
    #Criando instancias
    baseline = Baseline(COLLECTTION_PATH, BASELINE_PATH, WINDOW_SIZE)
    clearData = ClearData(BASELINE_PATH)

    #Chamando metodos de execucao
    print(baseline.execution()[0])
    print(clearData.execution()[0])