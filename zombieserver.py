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

def broadcast(conn, addr):
	#num_connected += 1
	p = PyAudio()

	#buffer
	#queue = deque([])
	data_list = []

	#when do we want to do this?
	while True:
		chunk = 1024
		FORMAT = paInt16
		CHANNELS = 1
		RATE = 8000
		RECORD_SECONDS = 10
		WAVE_OUTPUT_FILENAME = "output.wav"


		stream = p.open(format = FORMAT,
				        channels = CHANNELS,
				        rate = RATE,
				        input = True,
				        frames_per_buffer = chunk)

		print "* recording"
		all = []

		for i in range(0, RATE / chunk * RECORD_SECONDS):
			data = stream.read(chunk)		
			
			all.append(data)
			conn.sendall(data)
		print "* done recording"

		stream.close()
		p.terminate()
		'''
		print "* recording"
		for i in range(0, RATE / chunk * RECORD_SECONDS):
			data = stream.read(chunk)
			d = str(data)
			s = d.encode('hex_codec')
			data_list.append(s)
			conn.send(data_list[i])
		print "* done recording"

		stream.close()
		p.terminate()
		'''
#	i = 0

#	if i > len(data_list):
#		data_chunk = data_list[i]
#		i += 1
#		data_chunk = queue.popleft()
#		conn.send(data_chunk)
#	else:
#		i = 0
        


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
