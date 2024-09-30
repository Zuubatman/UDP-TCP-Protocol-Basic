from socket import *
import threading
serverName = 'localhost'

serverPort = 40000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(2)

# message = input('Input lowercase sentence:')

# clientSocket.sendto(message.encode(),(serverName, serverPort))
# modifiedMessage, serverAddress = clientSocket.recvfrom(2048)

# print (modifiedMessage.decode())

# clientSocket.close()


def listen():
    while(True):
        try:
            response, _  = clientSocket.recvfrom(2048)

            if(response.upper() == 'END'):
                clientSocket.close()
                break

            print (response.decode())
            
        except timeout:  
            continue  

        except  ():
            if not threading.main_thread().is_alive(): break
        
def sendToServer():    
    print("Insert a Command:")
    while(True):
        command = input("")
        
        if('pmf' in command):
            dataArr = command.split(' ')
            userDestination = dataArr[1]
            
            filePath = input("Insert file path:")
            with open(filePath, 'rb') as file:
                content = file.read()
               
            message = 'file '+ userDestination+ ' <file> \n'+ content.decode() 
            clientSocket.sendto(message.encode(),(serverName, serverPort))
    
        else:
            clientSocket.sendto(command.encode(),(serverName, serverPort))

def run():
    threading.Thread(target=listen).start()
    threading.Thread(target=sendToServer).start()

run()    
    