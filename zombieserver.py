from struct import *
import os,sys
import thread
from pyaudio import *
from socket import *
from collections import deque
import wave

__author__ =  'Ethan Genz, Jordan Haber, Eddie Figueroa'
__version__=  '1.0'

'''
Server-side for our ZombieComm Radio Broadcast.
'''

HOST = 'localhost'
PORT = 8080
num_connected = 0
recording = True

data_list = []


def record():

	'''
	Record from mic and append to list.
	'''

	global data_list

	p = PyAudio()

	chunk = 1024
	FORMAT = paInt16
	CHANNELS = 1
	RATE = 8000
	RECORD_SECONDS = 5

	stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = chunk)
	
	data_list = []

	print "* recording"

	for i in range(0, RATE / chunk * RECORD_SECONDS):
		data = stream.read(chunk)		
		data_list.append(data)

	print "* done recording"
	
	stream.close()
	p.terminate()


def broadcast(conn, addr):

	'''
	Send broadcast to client.
	'''
	
	global data_list

	#We use deque because it is thread-safe and quick.
	queue = deque([])
	for line in data_list:
		queue.append(line)

	print "Total connected: " + str(num_connected)
	
	while True:
		conn.send(queue.popleft())
		if len(queue) < 1:
			for line in data_list:
				queue.append(line)

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

	record()

	while True:
		clientsock, clientaddr = s.accept()
		thread.start_new_thread(broadcast, (clientsock, clientaddr))   
		num_connected += 1
	s.close()
