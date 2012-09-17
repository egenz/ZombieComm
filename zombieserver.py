import thread,sys
from socket import *
        
def main():
    try:
        server_sock = socket(AF_INET, SOCK_STREAM)
        server_sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        server_sock.bind(('localhost', 1337))
        server_sock.listen(200)
    
    except error, (value, message):
        if server_sock:
            server_sock.close()
        print "Could not open socket:", message
        sys.exit(1)

    while True:
        clientsock, clientaddr = server_sock.accept()
        thread.start_new_thread(proxy, (clientsock, clientaddr))
        
    server_sock.close()

def proxy(client_sock, client_addr):

    request = client_sock.recv(1049000)

    try:
        s = socket(AF_INET, SOCK_STREAM)  
        s.connect((URL, 80))
        s.send(request)

        while True:
            serverdata = s.recv(1049000)
            if (len(serverdata) > 0):
                client_sock.send(serverdata)
            else:
                break
        s.close()
        client_sock.close()
        
    except error, (value, message):
        if s:
            s.close()
        if client_sock:
            client_sock.close()
        print "Runtime Error:", message
        sys.exit(1)

if __name__ == '__main__':
    main()
