import socket, sys
import pickle

class ServerConnection():

    def __init__(self):
        
        try:
            # create an INET, STREAMing socket
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        except socket.error:
            print("Failed to create socket")
            sys.exit()
        else:
            print("Socket created")

    def connect(self, host, port):
        
        self.host = host
        self.port = port
        
        try:
            self.socket.connect((self.host, self.port))
        except OSError:
            print("Failed to connect to " + self.host + ":" + str(self.port))
            return False 
        else:
            print("Successfully connected to " + self.host + ":" + str(self.port))
            return True

    def send(self, data):
        binarydata = pickle.dumps(data)
        self.socket.sendall(binarydata)    
    
    def receive(self):
        binarydata = self.socket.recv(1024)
        data = pickle.loads(binarydata)
        return data