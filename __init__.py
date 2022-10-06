from .server import Server 
from .client import Client 
from .gui import GUI 

def server():
    ip = input('Enter ip address for server: ')
    port = int(input('Enter port number for server: '))
    n = int(input('Enter number of points on the screen: '))
    Server(ip, port, n)

def client():
    tcp_server_ip = input('Enter client\'s ip address: ')
    tcp_server_port = int(input('Enter tcp server port for client: '))
    is_slow_network = int(input('Is it a slow connection (0 for no, 1 for yes): '))
    gui = GUI()
    client = Client(tcp_server_ip, tcp_server_port, gui, is_slow_network)
    gui.set_client(client)
    gui.show()