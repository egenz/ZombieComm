from struct import *
import os,sys, time
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

data_list = []

s = None

def record(_seconds):

	'''
	Record from mic and append to list.
	'''

	global data_list

	p = PyAudio()

	chunk = 1024
	FORMAT = paInt16
	CHANNELS = 1
	RATE = 8000

	stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = chunk)
	
	tmp = []

	print "* recording"

	for i in range(0, RATE / chunk * _seconds):
		data = stream.read(chunk)		
		tmp.append(data)

	print "* done recording"
	data_list = tmp[:]
	stream.close()
	p.terminate()


def broadcast(conn, addr):

	'''
	Send broadcast to client.
	'''
	
	global data_list
	buffer_size = 3

	#We use deque because it is thread-safe and quick.
	queue = deque([])
	for line in data_list:
		queue.append(line)

	#print "Total connected: " + str(num_connected)
	
	while True:
		time.sleep(.045)
		try:
			if len(queue) > 0:
				conn.send(queue.popleft())
			if len(queue) == 0:
				for line in data_list:
					queue.append(line)
		except:
			pass

	conn.close()


def input_listener(_socket):

	while True:
		i = raw_input('[m] to record a new broadcast\n[q] to terminate server\n')
		if i == 'm':
			t = raw_input('enter recording length [seconds]\n')
			record(int(t))
		if i == 'q':
			_socket.close()
			os._exit(1)


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

	thread.start_new_thread(input_listener, (s,))   

	while True:
		clientsock, clientaddr = s.accept()
		thread.start_new_thread(broadcast, (clientsock, clientaddr))   
		num_connected += 1
	s.close()
