import pickle as p

#Metodo que retorna o array com todas as janelas de tempo
def openWindows():
    arq = open("Data structure\\CLEAR_WINDOWS.pickle", "rb")

    temp = p.load(arq)
    arq.close()

    return temp

#Metodo que retorna o dicionario que quantifica a frequencia dos enderecos MACs
def getClassifier(windows):
    count = 0
    dic = {}
    while count < len(windows):
        for mac in windows[count]:
            aux = windows[count]
            if aux[mac][0] <= -65 and aux[mac][1] >= 18:
                if mac in dic:
                    dic[mac] += 1
                else:
                    dic[mac] = 1
        count += 1
    return dic

#Metodo que imprime os enderecos macs a serem classificados como de um ocupante permanente
def getValidMacs(classifier):
    print("ENDEREÇOS MACS CLASSIFICADOS")
    count = 0
    for mac in classifier:
        if classifier[mac] >= 3:
            print("Endereço MAC %d: %s"%(count+1, mac))
            count+=1

windows = openWindows()
classifier = getClassifier(windows)
print(classifier)

getValidMacs(classifier)

######################################################PENDENCIAS########################################################
#Faltam parametros mais consistentes e salvar os dados gerados pelos inconsistentes a fim de realizar uma melhor analise
#Lembrar tambem de salvar os MACs que foram classificados como nao ocupantes


