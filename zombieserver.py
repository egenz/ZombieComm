import os,sys
import thread
import pyaudio
from socket import *

HOST = 'localhost'
PORT = 8080
        
def main():
    try:
        s = socket(AF_INET, SOCK_STREAM)
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(200)
    
    except error, (value, message):
        if s:
            s.close()
        print "Could not open socket:", message
        sys.exit(1)

    while True:
        clientsock, clientaddr = s.accept()
        thread.start_new_thread(broadcast, (clientsock, clientaddr))   
    s.close()

def broadcast(conn, addr):
    try:
        s = socket(AF_INET, SOCK_STREAM)  
        s.connect((HOST, PORT))

        while True:
            data = s.recv(1049000)
            if not data: break
            conn.send(serverdata)
        s.close()
        conn.close()
        
    except error, (value, message):
        if s:
            s.close()
        if conn:
            conn.close()
        print "Runtime Error:", message
        sys.exit(1)

if __name__ == '__main__':
    main()
