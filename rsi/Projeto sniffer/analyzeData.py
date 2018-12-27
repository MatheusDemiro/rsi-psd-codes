import pickle as p

#Metodo que retorna a lista com as janelas de captura limpas
def clearMAC(windows):
    count = 0
    clearWindows = []
    while count < len(windows):
        auxFake, auxWindow, auxIntel = [], {}, []
        for MAC in windows[count]:
            mac = MAC.split(":")
            result = "0x" + mac[0]
            if int(result, 16) & 2 == 2:  #MAC local (falso)
                auxFake.append(MAC)
                continue
            else:  #MAC universal
                if ":".join(mac[:3]) == "60:67:20":  #Se for do fornecedor "Intel Corporate"
                    if MAC not in auxIntel:
                        auxIntel.append(MAC)
                        continue
            auxWindow[MAC] = windows[count][MAC]
        count+=1
        if auxFake == []:
            auxFake.append(0)
        elif auxIntel == []:
            auxIntel.append(0)
        fakeMACWindow.append(auxFake);clearWindows.append(auxWindow);intelCorporateMACWindow.append(auxIntel)

    return clearWindows

#Metodo que exibe a quantidade de pacotes capturados por janela
def getAllPacketsWindow(dic):
    print("QUANTIDADE TOTAL DE ENDERECOS CAPTURADOS POR JANELA (FREQ. 15)\n")
    count = 0
    while count < len(dic):
        packets = 0
        for i in dic[count].keys():
            if dic[count][i][1] >= 15 and dic[count][i][0] <= -75:
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
        print("Janela %d: %d enderecos MACs falsos de %d MACs capturados" % (window, aux, len(windows[count])))
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
    while count < len(fakeMACWindow):
        aux = valuesF[count]+valuesI[count]
        print("Janela %d: %d enderecos MACs a ser desconsiderados."%(count+1, aux))
        off['result'][count] = aux
        count+=1
    return

#Metodo que exibe o resultado final da analise, sendo subtraidos os valores: (total de MACs a serem desconsiderados por janela)-(total de capturas por) janela
def getFinalResult():
    print("TOTAL POR JANELA A SER CONSIDERADO\n")
    for i in range(len(off['result'])):
        aux = off['result'][i]
        if aux < 0:
            aux *=(-1)
        print("Janela %d: %d enderecos MACs a serem considerados."%(i+1, abs(len(windows[i])-aux)))
    return

#Metodo que retorna todos os arrays e dicionarios utilizados para analise
def openWindows():
    arq = open("WINDOWS.pickle", "rb")

    temp = p.load(arq)
    arq.close()

    return temp

allIntelCorporateMAC, fakeMACWindow, intelCorporateMACWindow = [], [],[]
windows = openWindows()
clearWindows = clearMAC(windows)
off = {}

analysisFakeMACWindows(fakeMACWindow)
print("\n#############################################################################==#############################################################################\n")
analysisIntelCorporateMAC(intelCorporateMACWindow)
print("\n#############################################################################==#############################################################################\n")
totalOff()
print("\n#############################################################################==#############################################################################\n")
getFinalResult()
print("\n#############################################################################==#############################################################################\n")
getAllPacketsWindow(clearWindows)
