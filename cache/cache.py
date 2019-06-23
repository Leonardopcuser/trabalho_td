import socket
import sys

# Criando servidor socket e comecando a escutar
Serv_Port = 8080
Serv_Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# Preparando servidor socket
print "Abrindo conexao ..."
Serv_Sock.bind(('127.0.0.1', Serv_Port))
Serv_Sock.listen(5)



def caching_object(splitMessage, Cli_Sock):
    #Armazenamento em Cache
    Req_Type = splitMessage[0]
    Req_path = splitMessage[1]
    tam = len(Req_path)
    Req_path = Req_path[7:tam-1]
    print "Requisicao ", Req_Type, " URL : ", Req_path

    #Avaliando se existe arquivo na cache
    file_to_use = "/" + Req_path
    print file_to_use
    try:
        file = open(file_to_use[1:], "r")
        data = file.readlines()
        print "Arquivo presente em Cache!\n"

        

        #Servidor Proxy enviando dados
        for i in range(0, len(data)):
            Cli_Sock.send(data[i])
        print "Lendo arquivo da cache\n"

        
    except IOError:
        print "Arquivo nao existe em cache"
        serv_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_name = Req_path
        try:
            serv_proxy.connect((host_name, 80))
            fileobj = serv_proxy.makefile('r', 0)
            fileobj.write("GET " + "http://" + Req_path + " HTTP/1.0\n\n")

            
            buffer = fileobj.readlines()
    
            tmpFile = open("./" + Req_path, "wb")
            for i in range(0, len(buffer)):
                tmpFile.write(buffer[i])
                Cli_Sock.send(buffer[i])
        except:
            print 'Requisicao inviavel'

    Cli_Sock.close()
while True:
    # Recebendo do cliente
    print 'Iniciando servidor...\n '
    Cli_Sock, addr = Serv_Sock.accept() 
    message = Cli_Sock.recv(1024) 

    splitMessage = message.split()
    if len(splitMessage) <= 1:
        continue

    caching_object(splitMessage, Cli_Sock)
