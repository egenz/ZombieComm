import wave, threading
from pyaudio import *
from socket import *
from collections import deque


class Client(threading.Thread):

    def __init__(self, _host, _port):
        threading.Thread.__init__(self)

        self.client = socket(AF_INET, SOCK_STREAM)
        self.client.connect((_host, _port))

        self.queue = deque([])

    def run(self):

        while True:
            data = self.client.recv(1024)
            self.queue.append(data)


class Streamer(threading.Thread):

    def __init__(self, _client):
        threading.Thread.__init__(self)
        self.client = _client
        self.buffer_size = 6
        self.chunk = 1024

    def run(self):

        p = PyAudio()

        stream = p.open(format = data_format, channels = data_channels, rate = data_rate, output = True)
        
        while True:

            if len(self.client.queue) > self.buffer_size:
                
                stream.write(self.client.queue.popleft())
		
        stream.close()
        p.terminate()

    def save(self):

        FORMAT = paInt16
        CHANNELS = 1
        RATE = 8000

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
