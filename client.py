import wave, threading
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

        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect((_host, _port))

        self.queue = deque([])

    def run(self):
	'''
	Receive from server, append to buffer.
	'''
        while True:
            data = self.client.recv(1024)
            self.queue.append(data)


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

    def save(self):
		'''
		Write to buffer.
		'''
        data = wave.open('outfile.wav', 'wb')
        data.setnchannels(CHANNELS)
        data.setsampwidth(p.get_sample_size(FORMAT))
        data.setframerate(RATE)

        data_format = p.get_format_from_width(data.getsampwidth())
        data_channels = data.getnchannels()
        data_rate = data.getframerate()
                
        data.writeframes(self.client.queue[0])


if __name__ == '__main__':

    HOST = 'localhost'
    PORT = 8080

    c = Client(HOST, PORT)
    s = Streamer(c)
    c.start()
    s.start()
