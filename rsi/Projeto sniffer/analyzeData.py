import pickle as p

#Metodo que exibe a quantidade de pacotes capturados por janela
def getAllPacketsWindow(windows):
    print("\nQUANTIDADE TOTAL DE ENDERECOS CAPTURADOS POR JANELA (FREQ. 19)\n")
    count = 0
    while count < len(windows):
        packets = 0
        for i in windows[count].keys():
            if windows[count][i][1] > 19:
                packets += 1
        off['result'][count] -= packets
        count += 1
        print("Janela %d: %d enderecos MACs capturados."%(count, packets))
    return

#Metodo que exibe a quantidade de enderecos MACs falsos capturados em cada janela e retorna os totais com repeticao e sem repeticao (OBS.: os enderecos macs nao possuem repeticao na janela, porem podem aparecer mais de uma vez em janelas distintas)
def analysisFakeMACWindows(arrayMAC):
    print("\nQUANTIDADE DE ENDERECOS MACS FALSOS POR JANELA\n")

    window, count, total, unique = 0, 0, 0, 0
    off['fakeMAC'], arrayAux = {}, []
    while count < len(arrayMAC):
        window += 1
        aux = len(arrayMAC[count])
        print("Janela %d: %d enderecos MACs falsos" % (window, aux))
        for i in arrayMAC[count]:
            if i not in arrayAux:
                arrayAux.append(i)
        count+=1
        total+=aux
        off['fakeMAC'][count] = aux

    print("\nTotal de enderecos MACs falsos (com repeticoes): %d" % (total))
    print("Total de enderecos MACs falsos (sem repeticoes): %d" % (len(arrayAux)))

    return

#Metodo que exibe a quantidade de enderecos MACs da Intel Corporate (computadores do laboratorio) e os totais com repeticao e sem repeticao
def analysisIntelCorporateMAC(arrayIntelCorporate):
    print("QUANTIDADE DE ENDERECOS MACS DA INTEL CORPORATE\n")

    window, count, total = 0, 0, 0
    off['intelC'], arrayAux = {}, []
    while count < len(arrayIntelCorporate):
        window += 1
        aux = len(arrayIntelCorporate[count])
        print("Janela %d: %d enderecos MACs Intel Corporate" % (window, aux))
        for i in arrayIntelCorporate[count]:
            if i not in arrayAux:
                arrayAux.append(i)
        count += 1
        total += aux
        off['intelC'][count] = aux

    print("\nTotal de enderecos MACs da Intel Corporate (com repeticoes): %d" % (total))
    print("Total de enderecos MACs da Intel Corporate (sem repeticoes): %d" % (len(arrayAux)))

    return

#Metodo que exibe o total a desconsiderar por janela
def totalOff():
    print("TOTAL POR JANELA A SER DESCONSIDERADO\n")
    valuesF, valuesI = list(off['fakeMAC'].values()), list(off['intelC'].values())
    count = 0
    off['result'] = {}
    while count < len(valuesF):
        aux = valuesF[count]+valuesI[count]
        print("Janela %d: %d enderecos MACs a ser desconsiderados."%(count+1, aux))
        off['result'][count] = aux
        count+=1
    return

#Metodo que retorna todos os arrays e dicionarios utilizados para analise
def openAllArqs():
    arq, arq1, arq2 = open("WINDOWS.pickle", "rb"), open("fakeMACWindow.pickle", "rb"),open("intelCorporateMACWindow.pickle", "rb")
    x, y, z = p.load(arq), p.load(arq1), p.load(arq2)
    arq.close()
    arq1.close()
    arq2.close()

    return x,y,z

#Metodo que exibe o resultado final da analise, sendo subtraidos os valores: (total de MACs a serem desconsiderados por janela)-(total de capturas por) janela
def getFinalResult():
    print("TOTAL POR JANELA A SER CONSIDERADO\n")
    for i in range(len(off['result'])):
        aux = off['result'][i]
        if aux < 0:
            aux *=(-1)
        print("Janela %d: %d enderecos MACs a serem considerados."%(i+1, aux))
    return

windows, fakeMACwindow, intelCorporateMACWindow = openAllArqs()
off = {}

analysisFakeMACWindows(fakeMACwindow)
print("\n#############################################################################==#############################################################################\n")
analysisIntelCorporateMAC(intelCorporateMACWindow)
print("\n#############################################################################==#############################################################################\n")
totalOff()
getAllPacketsWindow(windows)
print("\n#############################################################################==#############################################################################\n")
getFinalResult()