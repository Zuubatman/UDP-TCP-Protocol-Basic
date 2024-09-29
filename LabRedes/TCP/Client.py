from socket import *
import threading

serverName = 'localhost'

serverPort = 12000
clientSocket = socket(AF_INET, SOCK_STREAM)


def listen():
    while(True):
        try:
            response = clientSocket.recv(1024).decode()

            if(response.upper() == 'END'):
                clientSocket.close()
                break

            print (response)

        except  ():
            if not threading.main_thread().is_alive(): break
        
def sendToServer():
    while(True):
        command = input()
        clientSocket.send(command.encode())

def run():
    print("Starting Client...")
    clientSocket.connect((serverName,serverPort))
    print(F"Connected with server: {serverName}")
    threading.Thread(target=listen).start()
    threading.Thread(target=sendToServer).start()

run()    


        # while(True):
        #     try: 
        #         print("Insert a command:")
        #         command = input()
        #         clientSocket.send(command.encode())
        #         response = clientSocket.recv(1024)
        #         print ('From Server:', response.decode())
            
        #     except  ():
        #         if not threading.main_thread().is_alive(): break