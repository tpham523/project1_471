# This is mostly a util file for client.
import os
import sys
import socket

# Default directories of client and server
clientDir = "ClientFiles/"
serverDir = "ServerFiles/"

def sendFile(fileName, connSock, command):

    # Location of file in server and client
    filePath = clientDir + fileName
    serverPath = serverDir + fileName

    # Open file to read if file exists
    if os.path.exists(filePath):
        fileObj = open(filePath, "r")
    else:
        print("File not found")
        return

    # Encode command and send it to socket
    command = command.encode()
    connSock.send(command)

    # Create another socket for transferring data
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dataSocket.bind(("", 0))

    # Send the encoded port number ('0.0.0.0', '0')
    connSock.send(str(dataSocket.getsockname()[1]).encode())
    dataSocket.listen(1)

    # Number of bytes sent
    numSent = 0

    # File data
    fileData = None

    # Acception connections
    connectionSocket, addr = dataSocket.accept()

    # Keep sending until all is sent
    while True:  
        
        # Read data then encode it
        fileData = fileObj.read()
        fileData = fileData.encode()
        print(fileData)

        # Make sure we did not hit EOF
        if fileData:
            
            # Get the size of data read
            # and convert it so string
            dataSizeStr = str(len(fileData))

            # Prepend 0's to the size string 
            # until the size is 10 bytes
            while len(dataSizeStr) < 10:
                dataSizeStr = "0" + dataSizeStr

            # Prepend the size of data to the file data
            fileData = dataSizeStr.encode() + fileData
            
            # Send all data
            while len(fileData) > numSent:
                numSent += connectionSocket.send(fileData[numSent:])
                print(numSent)

            uploadedFile = open(serverPath, "w")
            uploadedFile.write(fileData.decode())

        else:
            print("Done uploading.")
            break

    print(f"Sent {numSent} bytes ")

    fileObj.close()
    uploadedFile.close()
    connectionSocket.close()
    
def quit(connSock, command):
    command = command.encode()
    connSock.send(command)
        

    
    
    


