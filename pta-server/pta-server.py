# -*- coding: cp1252 -*-
from socket import *
import os

def getUserList():
    arq = open("users.txt","r")
    userList = [line.rstrip() for line in arq]
    arq.close()
    return userList    

serverPort = 11550
#Cria o Socket TCP (SOCK_STREAM) para rede IPv4 (AF_INET)
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('',serverPort))
#Socket fica ouvindo conexoes. O valor 1 indica que uma conexao pode ficar na fila
serverSocket.listen(1)

print("Servidor pronto para receber mensagens. Digite Ctrl+C para terminar.")

autentication = False #Flag
connectionSocket = None
usersList = getUserList() #Lista com usuarios
path = os.getcwd()+"\\files" #Diretorio dos arquivos

while 1:
   try:
        if autentication == False:
            #So ira aceitar comandos quando receber um usuario valido
            #Cria um socket para tratar a conexao do cliente
            connectionSocket, addr = serverSocket.accept()
            sentence = str(connectionSocket.recv(1024)).split() #Recebendo mensagem do servidor (atenticacao como primeiro envio)
            if len(sentence) == 3: #Verificando formato
                print(" ".join(sentence)) #Para exibir os pedidos requisitados pelo cliente
                if sentence[1] == "CUMP":
                    if sentence[2] in usersList: #Autenticando o usuário
                        connectionSocket.send(sentence[0]+" OK")
                        autentication = True
                        continue
                    else:
                        connectionSocket.send(sentence[0]+" NOK")
                        connectionSocket.close()
                        continue
                else:
                    connectionSocket.send(sentence[0]+" NOK")
                    connectionSocket.close()
                    continue
            else:
                connectionSocket.send(sentence[0]+" NOK")
                continue
        else:#Usuario autenticado
            #Setando diretorio para a pasta dos arquivos
            os.chdir(path)
            sentence = str(connectionSocket.recv(1024)).split()
            print(" ".join(sentence)) #Para exibir os pedidos requisitados pelo cliente
            if sentence[1] == "LIST" and len(sentence) == 2: #Verificando formato
                arqs = os.listdir(path)
                if arqs == []:
                    connectionSocket.send(sentence[0]+" NOK")
                    continue
                else:
                    connectionSocket.send(sentence[0]+" ARQS"+" "+str(len(arqs))+" "+",".join(arqs))
                    continue
            elif sentence[1] == "PEGA" and len(sentence) == 3: #Verificando formato
                try:
                    arq = open(sentence[2],"rb")
                    arqFormat = arq.read()
                    arq.close()
                    connectionSocket.send(sentence[0]+" ARQ"+" "+str(os.path.getsize(sentence[2]))+" "+arqFormat)
                except IOError:#Arquivo nao existe
                    connectionSocket.send(str(sentence[0])+" NOK")
            elif sentence[1] == "TERM" and len(sentence) == 2: #Verificando formato
                autentication = False #Reiniciando o processo de autenticação. Servidor pronto para receber novo usuário
                connectionSocket.send(sentence[0]+" OK")
                connectionSocket.close()
                continue
            else:
                connectionSocket.send(sentence[0]+" NOK")
                continue
            
   except (KeyboardInterrupt, SystemExit):
        break

serverSocket.close()
