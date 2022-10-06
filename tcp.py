from socket import *

class TCPServer():
    def __init__(self, ip, port, callback):
        self.ip = ip 
        self.port = port 
        self.bufferSize = 1024
        self.callback = callback
        self.TCPServerSocket = socket(family=AF_INET, type=SOCK_STREAM)
        self.TCPServerSocket.bind((self.ip, self.port))
        self.TCPServerSocket.listen(100)

        # print(f'TCP Server is up at {self.ip}:{self.port}')
    
    def up(self):
        while True:
            connectionSocket, addr = self.TCPServerSocket.accept()
            message = connectionSocket.recv(self.bufferSize).decode()
            # print(f'A message: {message} has come from {addr}')
            self.callback(connectionSocket, message)
            connectionSocket.close()

class TCPClient():
    def __init__(self, serverIP, serverPort):
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.bufferSize = 1024
        self.TCPClientSocket = socket(AF_INET, SOCK_STREAM)
        print(self.serverPort)
        print(type(self.serverPort))
        self.TCPClientSocket.connect((self.serverIP,int(self.serverPort)))

    def send_and_receive_data(self, data):
        self.TCPClientSocket.send(data.encode())
        server_message = self.TCPClientSocket.recv(self.bufferSize)
        return server_message.decode()
    
    def send_data(self, data):
        self.TCPClientSocket.send(data.encode())

    def close_connection(self):
        self.TCPClientSocket.close()

def get_a_tcp_client(ip, port):
    # print(f'A tcp client for server({ip}:{port}) is created.')
    return TCPClient(ip, port)