import socket
import sys 
import os

# Command line checks
if len(sys.argv) != 2:
    print(f"Usage: python3 {sys.argv[0]} <Port Number>")

listenPort = int(sys.argv[1])

welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
welcomeSock.bind(("",listenPort))
welcomeSock.listen(1)

def recvFile(sock, numBytes):
    
    recvBuff = ""
    tmpBuff = ""

    while len(recvBuff) < numBytes:
        tmpBuff = sock.recv(numBytes).decode()
        print(tmpBuff)

        if not tmpBuff:
            break
        
        recvBuff += tmpBuff

    print(recvBuff)
    
    return recvBuff


while True:

    print("Waiting for connections...")
    clientSock, addr = welcomeSock.accept()

    print(f"Accepted connection from client: {addr}\n")

    while True:

        command = clientSock.recv(1024)
        command = command.decode()

        if command == "put":

            clientPort = int(clientSock.recv(10).decode("utf-8"))

            servDataSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servDataSock.connect((addr[0], clientPort))

            fileData = ""
            recvBuff = ""

            fileSize = 0
            fileSizeBuff = ""

            fileSizeBuff = recvFile(servDataSock, 10) 
            print(fileSizeBuff)
            fileSize = int(fileSizeBuff)

            print(f"The file size is {fileSize}")

            fileData = recvFile(servDataSock, fileSize)

            print(f"The file data is: {fileData}\n")

        elif command == "quit":
            print("Goodbye")
            break
    break

clientSock.close()




