from struct import *
import os,sys
import thread
from pyaudio import *
from socket import *
from collections import deque
import wave

HOST = 'localhost'
PORT = 8080
num_connected = 0
recording = True

data_list = []


def broadcast(conn, addr):

	global num_connected
	num_connected += 1
	print "Total connected: " + str(num_connected)
	
	p = PyAudio()

	while True:
		chunk = 1024
		FORMAT = paInt16
		CHANNELS = 1
		RATE = 8000
		RECORD_SECONDS = 30

		stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = chunk)

		print "* recording"
		all = []

		for i in range(0, RATE / chunk * RECORD_SECONDS):
			data = stream.read(chunk)		
			
			all.append(data)
			conn.sendall(data)
		print "* done recording"

		stream.close()
		p.terminate()

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
