from algorithms.Classifier import Classifier
from algorithms.CreateWindow import CreateWindow

WINDOW_SIZE = 120 #1 minuto
CLEAR_COLLECTION_PATH = "data_structure\\(CLEAR)COLETA_PBD_13-12-18"
BASELINE_PATH = "data_structure\\BASELINE.pickle"

AVERAGE_FREQ = 5
AVERAGE_RSSI = -80

#Se o arquivo de execucao for o modulo principal
if __name__ == "__main__":
    #Criando instancias e chamando os respectivos metodos de execucao
    createWindow = CreateWindow(CLEAR_COLLECTION_PATH, WINDOW_SIZE)
    windows = createWindow.execution()
    classifier = Classifier(BASELINE_PATH, AVERAGE_RSSI, AVERAGE_FREQ, windows)
    exe = classifier.execution()
