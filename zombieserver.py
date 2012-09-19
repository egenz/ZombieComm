import os,sys
import thread
from pyaudio import *
from socket import *
from collections import deque
import wave

HOST = 'localhost'
PORT = 8080
num_connected = 0

def broadcast(conn, addr):
	num_connected += 1
	p = PyAudio()

	#buffer
	queue = deque([])

	while recording:
		chunk = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 1
		RATE = 44100
		RECORD_SECONDS = 5
		WAVE_OUTPUT_FILENAME = "output.wav"

		#p = pyaudio.PyAudio()

		stream = p.open(format = FORMAT,
						channels = CHANNELS,
						rate = RATE,
						input = True,
						output = True,
						frames_per_buffer = chunk)

		print "* recording"
		for i in range(0, RATE / chunk * RECORD_SECONDS):
			data = stream.read(chunk)
#			stream.write(data, chunk)
			queue.append(data)
		print "* done recording"

#		stream.stop_stream()
		stream.close()
		p.terminate()
		
		'''
		# write data to WAVE file
		data = ''.join(queue)
		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(data)
		wf.close()
		'''
		
		#if num_connected > 2:
		#lower audio stream
		

		if len(queue) > 6:
			data_chunk = queue.popleft()
			conn.send(data_chunk)
        

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
