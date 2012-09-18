import os,sys
import thread
from pyaudio import *
from socket import *
from collections import deque

HOST = 'localhost'
PORT = 8080

def broadcast(conn, addr):
    p = PyAudio()
    
    #buffer
    queue = deque([])

    while recording:
        #record stuff
        queue.append(chunk)
        if len(queue) > 6:
            data = queue.popleft()
            conn.send(data)
        
'''        
        with interleaving, how could we differentiate among the packets if they're
        out of order?
              
        #interleaving code
        if len(queue) > 6:
            data = ""
            data += str(queue.popleft(0))
            data += str(queue.popleft(3))
            data += str(queue.popleft(6))
            conn.send(data)
'''            
            
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
