from socket import *
from multiprocessing import current_process
serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))
sentence = input("input lowercase sentence: ").strip()
clientSocket.send(sentence.encode())
modifiedSentence = clientSocket.recv(1024)
print("From server:", modifiedSentence.decode())
clientSocket.close()

current_process().name