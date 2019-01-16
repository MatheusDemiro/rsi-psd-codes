from algorithms.Classifier import Classifier
from algorithms.CreateWindow import CreateWindow

WINDOW_SIZE = 60
CLEAR_COLLECTION_PATH = "data_structure\\(CLEAR)COLETA_PBD_13-12-18"
BASELINE_PATH = "data_structure\\BASELINE.pickle"
UNIQUE_MACS_PATH = "data_structure\\UNIQUE_MACS_PBD_13-12-18"

FREQUENCY = 10
AVERAGE_RSSI = -70

print("\n%d segundos"%(WINDOW_SIZE))
#Se o arquivo de execucao for o modulo principal
if __name__ == "__main__":
    #Criando instancias e chamando os respectivos metodos de execucao
    createWindow = CreateWindow(CLEAR_COLLECTION_PATH, WINDOW_SIZE, UNIQUE_MACS_PATH)
    WINDOWS = createWindow.execution()

    classifier = Classifier(BASELINE_PATH, WINDOWS, FREQUENCY, AVERAGE_RSSI)
    exe = classifier.execution()

"""OBS.: Todos os resultados acima estão corretos segundo a comparação com o baseline, apesar de alguns resultados 
apresentarem listas com zeros devido a janela não ser divisível por 5"""