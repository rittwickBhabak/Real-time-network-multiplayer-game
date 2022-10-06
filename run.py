import threading
import time
from client import make_client 
from server import make_server

threads = []
server = threading.Thread(target=make_server, args=("127.0.0.2", 20002, 3))
server.start()
time.sleep(2)
client_tcp_ports = [("127.0.0.2",30001, 0, "127.0.0.2", 20002), ("127.0.0.3",30004, 0, "127.0.0.2", 20002), ("127.0.0.10",30010, 1, "127.0.0.2", 20002)]
for port in client_tcp_ports:
    thread = threading.Thread(target=make_client, args=port)
    threads.append(thread)
    thread.start()

