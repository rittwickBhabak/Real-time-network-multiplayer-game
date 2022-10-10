from socket import *
import threading 
import json 

class Client():
    def __init__(self, ip, port, server_ip, server_port):
        self.ip = ip 
        self.port = port 
        self.buffer_size = 1024
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_socket.bind((self.ip, self.port))
        self.tcp_socket.listen(100)
        self.up_tcp_server()
        self.clients = [] 
        self.server_ip = server_ip 
        self.server_port = server_port 
        self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_client_socket.connect((self.server_ip, self.server_port))
        self.name = 'Rittwick'
        threading.Thread(target=self.send_different_req).start()

    def up_tcp_server(self):
        thread = threading.Thread(target=self.tcp_server)
        thread.start()
    
    def tcp_server(self):
        while True:
            connection_socket, addr = self.tcp_socket.accept()
            thread = threading.Thread(target=self.tcp_connection, args=(connection_socket, addr))
            thread.start()
    
    def tcp_connection(self, connection_socket, addr):
        while True:
            data = connection_socket.recv(self.buffer_size).decode()
            data = json.loads(data) 
            purpose = data.get('purpose')
            print(f'The purpose of the data is {purpose}')
            if purpose=='broadcast':
                message = data.get('message')
                print(f'Message from server: {message}')

    def send_different_req(self):
        while True:
            user_input = int(input('Enter 1 to first join\nEnter 2 to work more\nEnter 3 to wake up\n'))
            if user_input==1:
                self.tcp_client_socket.send(json.dumps({'purpose':'join-req', 'name':self.name, 'client-tcp-ip':self.ip, 'client-tcp-port':self.port}).encode())
                response = self.tcp_client_socket.recv(self.buffer_size).decode()
                response = json.loads(response) 
                client_id = response.get('id')
                self.client_id = client_id 
            elif user_input==2:
                self.tcp_client_socket.send(json.dumps({'purpose':'work', 'client-id':self.client_id}).encode())
                response = self.tcp_client_socket.recv(self.buffer_size).decode()
                response = json.loads(response) 
            else:
                self.tcp_client_socket.send(json.dumps({'purpose':'wake-up', 'client-id':self.client_id}).encode())
                response = self.tcp_client_socket.recv(self.buffer_size).decode()
                response = json.loads(response) 

            
            message = response.get('message')
            print(f'You got response {message}')

if __name__=='__main__':
    Client("10.194.38.53", 30000, "10.194.33.255", 20000)
    # Client("10.194.38.53", 30002, "10.194.33.255", 20000)
    # Client("10.194.38.53", 30003, "10.194.33.255", 20000)
