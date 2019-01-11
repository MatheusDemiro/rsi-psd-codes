from algorithms.collectData import CollectData
from algorithms.clearData import ClearData
from algorithms.result import Result
import os

#Se o arquivo de execucao for o modulo principal
if __name__ == "__main__":
    #Criando instancias
    collectData = CollectData(os.getcwd()+"\\Data\\COLETA_PBD_21-12-18.txt")
    clearData = ClearData("Data structure\\CLEAR_WINDOWS.pickle", "Data structure\\WINDOWS.pickle")
    result = Result("Data structure\\CLEAR_WINDOWS.pickle")

    #Chamando metodos de execucao
    collectData.execution()
    clearData.execution()
    result.execution()
