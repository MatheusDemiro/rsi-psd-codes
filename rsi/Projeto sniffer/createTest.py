from algorithms.Classifier import Classifier
from algorithms.CreateWindow import CreateWindow

WINDOW_SIZE = 10 #10 segundos
CLEAR_COLLECTION_PATH = "data_structure\\(CLEAR)COLETA_PBD_13-12-18"
BASELINE_PATH = "data_structure\\BASELINE.pickle"
UNIQUE_MACS_PATH = "data_structure\\UNIQUE_MACS_PBD_13-12-18"

# AVERAGE_FREQ = 8
# AVERAGE_RSSI = -80

#Se o arquivo de execucao for o modulo principal
if __name__ == "__main__":
    #Criando instancias e chamando os respectivos metodos de execucao
    createWindow = CreateWindow(CLEAR_COLLECTION_PATH, WINDOW_SIZE, UNIQUE_MACS_PATH)
    windows = createWindow.execution()
    print(windows)
    classifier = Classifier(BASELINE_PATH, windows)
    exe = classifier.execution()
