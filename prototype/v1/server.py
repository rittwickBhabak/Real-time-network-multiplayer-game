import json
from socket import *
import threading 

class Server():
    def __init__(self, ip, port):
        self.ip = ip 
        self.port = port 
        self.buffer_size = 1024
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_socket.bind((self.ip, self.port))
        self.tcp_socket.listen(100)
        self.up_tcp_server()
        self.clients = [] 

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
            if purpose=='join-req':
                client_id = len(self.clients) + 1 
                name = data.get('name')
                client_tcp_ip = data.get('client-tcp-ip')
                client_tcp_port = data.get('client-tcp-port')
                client_tcp_socket = socket(AF_INET, SOCK_STREAM)
                client_tcp_socket.connect((client_tcp_ip, client_tcp_port))
                client_obj = {'id':client_id, 'name':name, 'client-tcp-socket':client_tcp_socket}
                self.clients.append(client_obj)
                response_obj = {'message': 'You are in'} 
                response_obj['purpose'] = 'join-reply'
                response_obj['message'] = f'Your id is {client_id}'
                response_obj['id'] = client_id
                connection_socket.send(json.dumps(response_obj).encode())
            elif purpose=='work':
                client_id = data.get('client-id')
                connection_socket.send(json.dumps({'purpose': 'work-more', 'message': 'You have to work more'}).encode())
                for c in self.clients:
                    c_id = c.get('id')
                    if client_id!=c_id:
                        c_tcp_socket = c.get('client-tcp-socket')
                        c_tcp_socket.send(json.dumps({'purpose':'broadcast', 'message':f'Listen, client {client_id} wants to {purpose}'}).encode())
            else:
                client_id = data.get('client-id')
                connection_socket.send(json.dumps({'purpose': 'wake-up', 'message': 'You have to first wake up'}).encode())
                for c in self.clients:
                    c_id = c.get('id')
                    if client_id!=c_id:
                        c_tcp_socket = c.get('client-tcp-socket')
                        c_tcp_socket.send(json.dumps({'purpose':'broadcast', 'message':f'Listen, client {client_id} wants to {purpose}'}).encode())


if __name__=='__main__':
    server = Server("10.194.55.160", 20000)