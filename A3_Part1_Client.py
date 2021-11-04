import random
import time
from socket import *

HOST = "datakomm.work"
PORT = 1301

clientSocket = None

def connectServer(host, port):
	#Attempts to establish TCP connection
	#:param host: The remote host to connect to. Can be domain (localhost, ntnu.no, etc), or IP address
    #:param port: TCP port to us
	#:return: True if connection succeds, False otherwise
	global clientSocket
	clientSocket = socket(AF_INET, SOCK_STREAM)
	try:
		clientSocket.connect((host, port))
		return True
	except IOError as e:
		print("ERROR: ", e)
		return False
	return False

def closeConnection():
	#Closes the connection
	#:return: True if action succeds, False otherwise
	global clientSocket
	try:
		clientSocket.close()
		return True
	except IOError as e:
		print("ERROR: ", e)
		return False
	return False

def requestServer(req):
	#:param req: The request to be sent to the server
	#:return: True if sent successfully, False otherwise
	global clientSocket
	try:
		clientSocket.send(message.encode(req))
		return True
	except IOError as e:
		print("ERROR: ", e)
		return False
	return False

def readResponse():
	#Waits for a response and returns it.
	#:return: = response from the server
	global clientSocket
	try:
		resp = clientSocket.recv(1024)
		return resp
	except IOError as e:
		return None
	return None

def clientTests():
	#Different test scenarios
	#:return: the result of the test
	print("Simple TCP client started")
	if not connectServer(HOST, PORT):
		return "ERROR: Failed to connect to the server"
	print("Connection to the server established")
	a = random.randint(1, 20)
	b = random.randint(1, 20)
	request = str(a) + "+" + str(b)
	
	if not requestServer(request):
		return "ERROR: Failed to send valid message to server!"
	
	print("sent ", request, " to server")
	response = readResponse()
	if response is None:
		return "ERROR: Failed to receive server's response!"
	
	print("Server responded with: ", response)
	secsToSlp = 2 + random.randint(0, 5)
    print("Sleeping %i seconds to allow simulate long client-server connection..." % secsToSlp)
    time.sleep(secsToSlp)
	
	request = "bla+bla"
	if not requestServer(request):
		return "ERROR: Failed to send invalid message to server!"
	
	print("sent ", request, " to server")
	response = readResponse()
	if response is None:
		return "ERROR: Failed to receive server's response!"
	
	print("Server responded with: ", response)
	if not (requestServer("game over") and closeConnection():
		return "ERROR: Could not finish the conversation with the server"
	
	print("Game over, connection closed")
	#Sends one last request after closing connection, should fail.
	if requestServer(request):
		return "ERROR: sending a message after closing the connection did not fail!"
	print("Sending another message after closing the connection failed as expected")
	return "Simple TCP client finished"

if __name__ == '__main__':
	result = clientTests()
	print(result)
