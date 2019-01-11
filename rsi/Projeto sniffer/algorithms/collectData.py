import pickle as p
import time

import serial

def setTimestamp(data):
        return data.decode()[:-2] + "," + str(int(time.time()))

if __name__ == "__main__":
    comport = serial.Serial('com10', 115200)
    arq = open("data structure\\data_sniffer.txt", "w+")

    while True:
        try:
            data = setTimestamp(comport.readline())
            if not data:
                break
            print(data)
            arq.writelines(data + "\n")
        except Exception:
            arq.close()
            comport.close()

#Para deteccoes com media de RSSI maior que 85 obtemos um totalRepetitions de 42 pacotes capturados, sendo que apenas 32 (16 pessoas e 16 maquinas)
#correspondem a realidade da sala de aula (observacao).
#Para a primeira janela de tempo admiti uma quantidade de aparicoes de 20 vezes com media de RSSI maior que 50, sendo coletados exatamente
#32 pacotes, que por mera coincidencia correspondem as 16 pessoas e 16 maquinas presentes em sala.

     ##############################################################################################################
###### OBS.: OS ENDERECOS MACs NAO POSSUEM REPETICAO NA JANELA, POREM PODEM APARECER MAIS DE UMA VEZ EM JANELAS DISTINTAS ######
     ##############################################################################################################
