import json
import time
from tkinter import *
import threading

from gui import CANVAS_HEIGHT, CANVAS_WIDTH, GUI 
from tcp import get_a_tcp_client, TCPServer 
from measurements import get_canvas_height, get_canvas_width 

CANVAS_HEIGHT = get_canvas_height()
CANVAS_WIDTH = get_canvas_width()

class Client():
    def __init__(self, tcp_server_ip, tcp_server_port, gui, is_slow_network=False):
        self.points = 0 
        self.tcp_server_ip = tcp_server_ip
        self.tcp_server_port = tcp_server_port
        self.gui = gui 
        self.is_slow_network = is_slow_network
        self.delay = 5

    def square_clicked(self, square_id, clicked_at, amount=5):
        self.points = self.points + amount
        self.gui.update_point_canvas(self.points)
        # print(f'Canvas updated by {self.points}')
        tcp_client = get_a_tcp_client(self.server_ip, self.server_port)

        if self.is_slow_network:
            time.sleep(self.delay)

        data = tcp_client.send_and_receive_data(json.dumps({'purpose':'click', 'square_id':square_id, 'player_id':self.player_id, 'clicked_at':str(clicked_at) }))
        data = json.loads(data)
        clicked_by = data.get('player_id')
        # print(data)
        if clicked_by != self.player_id:
            self.points = self.points - amount 
            self.gui.update_point_canvas(self.points)

    def show_status(self):
        tcp_client = get_a_tcp_client(self.server_ip, self.server_port)
        data = tcp_client.send_and_receive_data(json.dumps({"purpose":"game_over", "player_id":self.player_id}))
        data = json.loads(data)
        purpose = data.get('purpose')
        if purpose=='wait':
            self.gui.write_on_canvas(self.gui.canvas, 'Your game is over but wait for other players', CANVAS_WIDTH/2, CANVAS_HEIGHT/2)
        else:
            final_ranks = data.get('final_ranks')

            try:
                final_ranks = json.loads(final_ranks)
                final_ranks = final_ranks.get('final_ranks')
            except:
                pass 
            self.gui.show_final_status(final_ranks)
    
    def connect_to_server(self, server_ip, server_port, name):
        self.server_ip = server_ip 
        self.server_port = server_port 
        self.tcp_con_2 = TCPServer(self.tcp_server_ip, self.tcp_server_port, self.process_data)
        thread = threading.Thread(target=self.tcp_con_2.up) 
        thread.start()
        # print('Request sent from client...')
        tcp_client = get_a_tcp_client(self.server_ip, self.server_port)
        data = tcp_client.send_and_receive_data(json.dumps({'name':name,'ip':self.tcp_server_ip, 'port':self.tcp_server_port, 'purpose':'join'}))
        # print(f"Data: {data}")
        data = json.loads(data)
        # print(f'First Data from server is {data}')
        self.player_id = data.get('player_id')
        if self.is_slow_network:
            self.gui.root.title(f'Player {name} (Slow network)')
        else:
            self.gui.root.title(f'Player {name} ')
        coordinates = data.get('coordinates')
        start_time = data.get('start_time')
        return (start_time, coordinates)

    def process_data(self, connectionSocket, data):
        if self.is_slow_network:
            time.sleep(self.delay)
        # print('A req from server authority has came.')
        # data = connectionSocket.recv(1024).decode()
        data = json.loads(data) 
        # print(f'From Process Data: {data}')
        purpose = data.get('purpose')
        if purpose=='update_points':
            p_id = data.get('first_clicked_by')
            if p_id == self.player_id:
                self.points = self.points - 5 
                self.gui.update_point_canvas(self.new_point)
        elif purpose=='update_list':
            player_list = data.get('player_list')
            self.gui.update_player_list(player_list)
        elif purpose=='del_square':
            square_id = data.get('square_id')
            for square in self.gui.squares:
                s_id = square.get('id')
                if square_id==s_id:
                    obj = square.get('obj')
                    try:
                        self.gui.canvas.delete(obj)
                    except:
                        # the square is already deleted
                        pass 
                    self.gui.squares.remove(square)
                    if len(self.gui.squares)==0:
                        self.gui.on_game_end()
        elif purpose=='game_over':
            final_ranks = data.get('final_ranks')
            self.gui.show_final_status(final_ranks)
            
        

def make_client(tcp_server_ip, tcp_server_port, is_slow_network):
    gui = GUI()
    
    client = Client(tcp_server_ip, tcp_server_port, gui, is_slow_network)
    gui.set_client(client)   
    gui.show()


if __name__=='__main__':
    tcp_server_ip = input('Enter client\'s ip address: ')
    tcp_server_port = int(input('Enter tcp server port for client: '))
    is_slow_network = int(input('Is it a slow connection (0 for no, 1 for yes): '))
    gui = GUI()
    client = Client(tcp_server_ip, tcp_server_port, gui, is_slow_network)
    gui.set_client(client)
    gui.show()