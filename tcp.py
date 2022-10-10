from socket import *
import threading
import time

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
    
    def manage_connection(self, connectionSocket, addr):
        while True:
            message = connectionSocket.recv(self.bufferSize).decode()
            print(f'A message: {message} has come from {addr}')
            self.callback(connectionSocket, message)
            # connectionSocket.close()  

    def up(self):
        while True:
            connectionSocket, addr = self.TCPServerSocket.accept()
            thread = threading.Thread(target=self.manage_connection, args=(connectionSocket, addr))
            thread.start()
            

class TCPClient():
    def __init__(self, serverIP, serverPort, is_slow=False):
        self.serverIP = serverIP
        self.serverPort = serverPort
        self.delay = 5 
        self.is_slow = is_slow 
        self.bufferSize = 1024
        self.TCPClientSocket = socket(AF_INET, SOCK_STREAM)
        # print(self.serverPort)
        # print(type(self.serverPort))
        self.TCPClientSocket.connect((self.serverIP,int(self.serverPort)))

    def send_and_receive_data(self, data):
        if self.is_slow:
            time.sleep(self.delay)
        self.TCPClientSocket.send(data.encode())
        server_message = self.TCPClientSocket.recv(self.bufferSize)
        if self.is_slow:
            time.sleep(self.delay)
        # self.close_connection()
        return server_message.decode()
    
    def send_data(self, data):
        self.TCPClientSocket.send(data.encode())
        # self.close_connection()

    def close_connection(self):
        self.TCPClientSocket.close()
        print(f'A tcp client is destroyed.')

def get_a_tcp_client(ip, port, is_slow=False):
    print(f'A tcp client for server({ip}:{port}) is created.')
    return TCPClient(ip, port, is_slow)