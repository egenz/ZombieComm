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

        while True:

            if len(self.client.queue) > self.buffer_size:
                
                data = wave.open(self.client.queue.popleft(), 'rb')
                #data = wave.open('boing.wav','rb')

                p = PyAudio()

                data_format = p.get_format_from_width(data.getsampwidth())
                data_channels = data.getnchannels()
                data_rate = data.getframerate()

                stream = p.open(format = data_format, channels = data_channels, rate = data_rate, output = True)

                audio = data.readframes(self.chunk)
                while not audio == '':
                    stream.write(audio)
                    audio = data.readframes(self.chunk)

                stream.close()
                p.terminate()
                


if __name__ == '__main__':

    HOST = 'localhost'
    PORT = 8080

    c = Client(HOST, PORT)
    s = Streamer(c)
    c.start()
    s.start()
