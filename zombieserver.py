import os,sys
import thread
from pyaudio import *
from socket import *
from Queue import *

HOST = 'localhost'
PORT = 8080

def broadcast(conn, addr):
    p = PyAudio()
    
    #buffer
    q = Queue()

    while recording:
        #record stuff
        q.put(chunk)
        
        #if queue reaches 7 chunks of data, start sending
        #unsure if we want it to be 7 or not
        #chunks are just bits, right? we should be able to send it if that's the case
        if q.qsize() > 6:
            data = q.get()
            conn.send(data)
            
            
       #interleaving, work-in-progress     

    conn.send(data)
    s.close()
    conn.close()

if __name__ == '__main__':
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
