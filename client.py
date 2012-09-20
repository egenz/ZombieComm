import wave, threading, sys, os
from pyaudio import *
from socket import *
from collections import deque

__author__ =  'Ethan Genz, Jordan Haber, Eddie Figueroa'
__version__=  '1.0'

'''
Client-side for our ZombieComm Radio Broadcast.
'''

class Client(threading.Thread):

    def __init__(self, _host, _port):
        threading.Thread.__init__(self)

        try:
            self.client = socket(AF_INET, SOCK_STREAM)
            self.client.connect((_host, _port))
        except:
            print 'Broadcast server is unreachable'
            os._exit(1)
            

        self.queue = deque([])

        self.storage = []
        self.recording = False
        self.p = PyAudio()

    def run(self):
	'''
	Receive from server, append to buffer.
	'''
        while True:
            data = self.client.recv(1024)
            self.queue.append(data)
            if self.recording:
                self.storage.append(data)

    def record(self):
        if not self.recording:
            self.recording = True
        else:
            self.recording = False
            self.save()
            
    def save(self):
        '''
        Write to file.
        '''
        FORMAT = paInt16
        CHANNELS = 1
        RATE = 8000

        data = ''.join(self.storage)

        f = wave.open('broadcast.wav', 'wb')
        f.setnchannels(CHANNELS)
        f.setsampwidth(self.p.get_sample_size(FORMAT))
        f.setframerate(RATE)
        f.writeframes(data)
        f.close()

        self.storage = []


class Streamer(threading.Thread):

    def __init__(self, _client):
        threading.Thread.__init__(self)

        self.FORMAT = paInt16
        self.CHANNELS = 1
        self.RATE = 8000

        self.client = _client
        self.buffer_size = 6
        self.chunk = 1024

    def run(self):
        p = PyAudio()

        stream = p.open(format = self.FORMAT, channels = self.CHANNELS, rate = self.RATE, output = True)
        
        while True:

            if len(self.client.queue) > self.buffer_size:
                
                stream.write(self.client.queue.popleft())
		
        stream.close()
        p.terminate()


class listener(threading.Thread):

    def __init__(self, _client, _stream):
        threading.Thread.__init__(self)
        self.c = _client
        self.m = _stream


    def run(self):
         while True:
             if not self.c.recording:
                 i = raw_input('[r] to start recording broadcast\n[q] to terminate client\n')
                 if i == 'r':
                     self.c.record()
                     
                 if i == 'q':
                     self.c.client.close()
                     os._exit(1)
             if self.c.recording:
                 i = raw_input('[r] to stop recording broadcast\n')
                 if i == 'r':
                     self.c.record()
                     



if __name__ == '__main__':

    HOST = 'localhost'
    PORT = 8080

    c = Client(HOST, PORT)
    s = Streamer(c)
    l = listener(c, s)
    c.start()
    s.start()
    l.start()
