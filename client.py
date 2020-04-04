import socket
import os
import sys
from utils import sendFile, quit



if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <Server Machine> <Server Port>")

# Get server address and port
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

serverAddr = socket.gethostbyname(serverName)

# Create socket and connect to server 
connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connSock.connect((serverAddr, serverPort))

while True:
    # Break command into multiple parts

    command = input(">ftp ").split()
    print(len(command))

    if (command[0] == "put" and len(command) == 2):

            fileName = command[1]         
            sendFile(fileName, connSock, command[0])  
    
    elif command[0] == "quit":
            quit(connSock, command[0])
            break

    else:
        print("Invalid command.")

connSock.close()
print("Connection closed.")
# fileObj.close()


