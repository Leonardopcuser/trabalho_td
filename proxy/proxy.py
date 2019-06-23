import socket, sys, thread, httplib, re
from thread import *
from datetime import datetime

def start():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('127.0.0.1', 8080))
        s.listen(5)
        print "[+] Ouvindo as conexoes..."
    except Exception, e:
        print "[-] Nao foi possivel iniciar o socket. :("
        sys.exit(2)
    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(8192)
            start_new_thread(conn_string, (conn, addr, data))
        except KeyboardInterrupt:
            s.close()
            print "\n[-] Servidor Proxy finalizando..."
            print "[-] Saindo...\n"
            sys.exit(1)
    s.close()
def conn_string(conn, addr, data):
    try:
        firstline = data.split('\n')[0] 
        url = firstline.split(' ')[1] 
        http_pos = url.find('://')
	if(http_pos==-1):
		temp = url
	else:
		temp = url[(http_pos+3):] # armazena a url completa
        port_pos = temp.find(':') 
        webserver_pos = temp.find('/') # encontra o final da url
			
	arquivo1 = open('whitelist.txt', 'r')	
	for line1 in arquivo1:
		p1 = line1[0:line1.index('\n')]
		p2 = temp[0:temp.index('/')]
		if(p1==p2):    
            		print "\n[>] ACESSO AUTORIZADO: ", temp			
			datahora0 = datetime.now()
			datahora1 = datahora0.strftime('%d/%m/%Y %H:%M')			
			arquivo = open("logs.txt", "a")            		
			arquivo.write(datahora1 + " - [>] ACESSO AUTORIZADO: " + temp + "\n")
			arquivo.close()	
	
        if webserver_pos == -1: 
            webserver_pos = len(temp) 
        webserver = "" 
        port = -1 

        if (port_pos == -1 or webserver_pos < port_pos): 
            port = 80
            webserver = temp[:webserver_pos] # site raiz
        
	else:
	    port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
	    webserver = temp[:port_pos]
	proxy_server(webserver, port, conn, addr, data)    
    except Exception, e:
        pass
def proxy_server(webserver, port, conn, addr, data):  
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((webserver, port))
        s.send(data)
	ip_host=socket.gethostbyname(webserver)
	
	print "\n======================="    		
	print "\n- HOST:", webserver
    	print "\n- IP:", ip_host
	print "\n======================="

	arquivo = open('blacklist.txt', 'r')
	for line in arquivo:
		p1 = line[0:line.index('\n')]
		p2 = webserver
		if(p1==p2):    
            		print "\n[!] ACESSO NEGADO: ", webserver			
			datahora0 = datetime.now()
			datahora1 = datahora0.strftime('%d/%m/%Y %H:%M')			
			arquivo = open("logs.txt", "a")            		
			arquivo.write(datahora1 + " - [!] ACESSO NEGADO: " + webserver + "\n")
			arquivo.close()
			html='Acesso nao autorizado!'
            		conn.send(html)
            		s.send(html)
			conn.close()	
			s.close()
	
	while 1:
		reply = s.recv(8192)
		if(len(reply)>0):
			conn.send(reply)
		else:
			break
        s.close()
        conn.close()
	
    except socket.error, (value, message):
        s.close()
        conn.close()
        sys.exit(1)

start()

