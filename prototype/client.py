from datetime import datetime
from functools import partial
import time
from tkinter import * 
from socket import *
import threading 
import json 
from measurements import get_canvas_width, get_canvas_height, get_root_width, get_root_height, get_form_width, get_form_height, get_status_width, get_status_height, get_my_point_width, get_my_point_height, get_square_side_length

CANVAS_WIDTH = get_canvas_width()
CANVAS_HEIGHT = get_canvas_height()
ROOT_WIDTH = get_root_width()
ROOT_HEIGHT = get_root_height()
FORM_WIDTH = get_form_width()
FORM_HEIGHT = get_form_height()
STATUS_WIDTH = get_status_width()
STATUS_HEIGHT = get_status_height()
MY_POINT_WIDTH = get_my_point_width()
MY_POINT_HEIGHT = get_my_point_height()
SQUARE_SIDE_LENGTH = get_square_side_length()

class Client():
    def __init__(self, ip, port=30000, server_ip="", server_port=0, name="", is_slow=False, delay=5):
        self.ip = ip 
        self.port = port 
        self.buffer_size = 1024
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_socket.bind((self.ip, self.port))
        print(f'Tcp server is up at {self.ip}:{self.port}')
        self.tcp_socket.listen(100)
        self.up_tcp_server()
        self.server_ip = server_ip 
        self.server_port = server_port 
        self.name = name 
        self.points = 0
        self.is_slow = is_slow 
        self.delay = delay
        # threading.Thread(target=self.send_different_req).start()

        self.root = Tk()    
        self.root.geometry(f"{ROOT_WIDTH}x{ROOT_HEIGHT}")
        self.root.resizable(False, False)
        self.root.title('Real-time network multiplayer game')
        self.draw_blank_canvas()
        self.make_form()


    def up_tcp_server(self):
        thread = threading.Thread(target=self.tcp_server)
        thread.start()
    
    def tcp_server(self):
        print('TCP server is up in this client')
        while True:
            connection_socket, addr = self.tcp_socket.accept()
            thread = threading.Thread(target=self.tcp_connection, args=(connection_socket, addr))
            thread.start()
    
    def do_delay(self, data):
        if self.is_slow:
            time.sleep(self.delay)
        purpose = data.get('purpose')
        # purpose can be of the types
        # 'delete-square', 'update-points'
        if purpose=='delete-square':
            square_id = data.get('square-id')
            for square in self.squares:
                s_id = square.get('id')
                if square_id==s_id:
                    obj = square.get('obj')
                    try:
                        self.canvas.delete(obj)
                    except:
                        pass 
                    self.squares.remove(square)
                    if len(self.squares)==0:
                        self.on_game_end()
        elif purpose=='update-points':
            # p_id = data.get('actually-clicked-by')
            # if p_id == self.client_id:
            print(f'{self.client_id} have to decrease 5 points.')
            self.points = self.points - 5 
            self.update_point_canvas(self.points)
        elif purpose=='game-over':
            final_ranks = data.get('final-ranks')
            self.show_final_status(final_ranks)
        elif purpose=='quit':
            quit()


    def tcp_connection(self, connection_socket, addr):
        while True:
            data = connection_socket.recv(self.buffer_size).decode()
            print(f'The data is {data}')
            data = json.loads(data) 
            threading.Thread(target=self.do_delay, args=(data,)).start()

            
    def send_and_receive_data(self, data):
        # data will be of the type
        # {'purpose':'join-req', 'name':self.name, 'client-tcp-ip':self.ip, 'client-tcp-port':self.port}
        # {'purpose': 'square-click', 'square-id': square_id, 'clicked-at':clicked_at, 'clicked-by':client_id}
        # {'purpose': 'gave-over', 'client-id':client_id}
        # {'purpose': 'dis-connecting', 'client-id':client_id}
        self.tcp_client_socket.send(json.dumps(data).encode())
        response = self.tcp_client_socket.recv(self.buffer_size).decode()
        response = json.loads(response)
        return response 

    def make_form(self):
        self.form_frame = Frame(self.root, borderwidth=2, relief=GROOVE,)
        ip_label = Label(self.form_frame, text="Enter Server IP")
        port_label = Label(self.form_frame, text="Enter Server port")
        name_label = Label(self.form_frame, text="Enter name")
        self.ip_value = StringVar()
        self.port_value = IntVar()
        self.name_value = StringVar()
        ip_entry = Entry(self.form_frame, textvariable=self.ip_value)
        port_entry = Entry(self.form_frame, textvariable=self.port_value)
        name_entry = Entry(self.form_frame, textvariable=self.name_value)

        join_button = Button(self.form_frame, text='Join')
        join_button.bind('<Button-1>', partial(self.join_click_handler))
        join_button.bind('<Return>', partial(self.join_click_handler))

        ip_label.pack(side=LEFT)
        ip_entry.pack(side=LEFT)
        port_label.pack(side=LEFT)
        port_entry.pack(side=LEFT)
        name_label.pack(side=LEFT)
        name_entry.pack(side=LEFT)
        join_button.pack(side=LEFT)
        self.form_frame.pack(anchor='nw', side=BOTTOM, pady=20, padx=15)
        self.ip_value.set(self.server_ip)
        self.port_value.set(self.server_port)
        self.name_value.set(self.name)

    def draw_blank_canvas(self):
        self.canvas = Canvas(self.root, height=CANVAS_HEIGHT, width=CANVAS_WIDTH, relief=GROOVE, borderwidth=2)
        self.canvas.pack(anchor=W) 
        self.write_on_canvas(self.canvas, 'To start the game enter the server IP address and port number.', CANVAS_WIDTH/2, CANVAS_HEIGHT/2)       

    def blank_my_points(self):
        self.points_canvas = Canvas(self.root, height=MY_POINT_HEIGHT, width=MY_POINT_WIDTH, relief=GROOVE, borderwidth=2)
        self.points_canvas.create_text(MY_POINT_WIDTH/2, MY_POINT_HEIGHT/2, text='My Points: 0')
        self.points_canvas.pack(anchor=E, side=RIGHT)

    def clear_canvas(self, canvas):
        try:
            canvas.delete('all') 
        except:
            pass 

    def write_on_canvas(self, canvas, text, x, y):
        self.clear_canvas(canvas)
        try:
            canvas.create_text(x, y, text=text)
        except:
            pass 
    
    def join_click_handler(self, event):
        self.form_frame.destroy() 
        self.blank_my_points()

        self.server_ip = self.ip_value.get()
        self.server_port = self.port_value.get()
        self.tcp_client_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_client_socket.connect((self.server_ip, self.server_port))

        self.name = self.name_value.get()
        # print(ip, port, name)
        response = self.send_and_receive_data({'purpose':'join-req', 'name':self.name, 'client-tcp-ip':self.ip, 'client-tcp-port':self.port})
        self.client_id = response.get('client-id')
        self.coordinates = response.get('coordinates')
        self.game_starts_at = datetime.strptime(response.get('game-starts-at'), '%Y-%m-%d %H:%M:%S.%f')

        if self.is_slow:
            self.root.title(f'Player({self.client_id}) - {self.name} (slow network)')
        else:
            self.root.title(f'Player({self.client_id}) - {self.name}')
        thread = threading.Thread(target=self.draw_squares)
        thread.start()

    def draw_squares(self):
        self.clear_canvas(self.canvas)
        self.squares = []
        while datetime.now()<self.game_starts_at:
            continue 
        for coordinate in self.coordinates:
            square_id = coordinate.get('id')
            x0 = coordinate.get('x0')
            y0 = coordinate.get('y0')
            color = coordinate.get('color')
            square = self.canvas.create_rectangle(x0,y0,x0+SQUARE_SIDE_LENGTH,y0+SQUARE_SIDE_LENGTH, fill=color)
            self.squares.append({'id':square_id, 'x0':x0,'y0':y0,'obj':square})

        self.canvas.bind('<Button-1>', self.square_click_handler)

    def show(self):
        self.root.mainloop()

    def update_point_canvas(self, new_point):
        self.clear_canvas(self.points_canvas)
        self.write_on_canvas(self.points_canvas, f'My Points: {new_point}', MY_POINT_WIDTH/2, MY_POINT_HEIGHT/2)

    def square_click_handler(self, event):
        x = event.x
        y = event.y 
        temp = self.squares
        for square in temp:
            square_id = square.get('id')
            x0 = square.get('x0')
            y0 = square.get('y0')
            obj = square.get('obj')
            if x0<=x<=x0+SQUARE_SIDE_LENGTH and y0<=y<=y0+SQUARE_SIDE_LENGTH:
                self.canvas.delete(obj)
                self.squares.remove(square)
                print(f'Square({square_id}) is clicked on {datetime.now()} by {self.client_id}')
                thread = threading.Thread(target=self.square_clicked, args=(square_id, datetime.now()))
                thread.start()
                if len(self.squares)==0:
                    print(f'Now there are no more squares')
                    thread = threading.Thread(target=self.on_game_end)
                    thread.start()

    def on_game_end(self):
        self.clear_canvas(self.canvas)
        self.write_on_canvas(self.canvas, 'Game Over', CANVAS_WIDTH/2, CANVAS_HEIGHT/2)
        self.show_status()

    def handle_connections(self, square_id, clicked_at, amount=5):
        if self.is_slow:
            time.sleep(self.delay)
        response = self.send_and_receive_data({'purpose': 'square-click', 'square-id': square_id, 'clicked-at':str(clicked_at), 'clicked-by':self.client_id})
        if self.is_slow:
            time.sleep(self.delay)
        actually_clicked_by = response.get('actually-clicked-by')
        # print(data)
        if actually_clicked_by != self.client_id:
            self.points = self.points - amount 
            self.update_point_canvas(self.points)

    def square_clicked(self, square_id, clicked_at, amount=5):
        self.points = self.points + amount
        self.update_point_canvas(self.points)
        thread = threading.Thread(target=self.handle_connections, args=(square_id,clicked_at,amount))
        thread.start()

    def show_status(self):
        response = self.send_and_receive_data({'purpose': 'game-over', 'client-id':self.client_id})
        purpose = response.get('purpose')
        if purpose=='wait':
            self.write_on_canvas(self.canvas, 'Your game is over but wait for other players', get_canvas_width()/2, get_canvas_height()/2)
        else:
            temp_list = [1,2,3]
            final_ranks = response.get('final-ranks')
            if type(final_ranks)!=type(temp_list):
                final_ranks = json.loads(final_ranks)
                final_ranks = final_ranks.get('final_ranks')
            self.show_final_status(final_ranks)

    def show_final_status(self, final_ranks):
        self.canvas.destroy()
        self.points_canvas.destroy()
        frame = Frame(self.root, padx=20, pady=20)
        label1 = Label(frame, text="Game Over", font='times 24 bold')
        label2 = Label(frame, text=f"Your Points {self.points}", font='times 24 bold')
        label3 = Label(frame, text="Final Ranks", font='times 24 bold')
        exit_btn = Button(frame, text='Exit Game', command=self.close)

        listbox = Listbox(frame)
        final_ranks.sort(key=lambda x: x[2], reverse=True)
        for index, player in enumerate(final_ranks):
            listbox.insert(index+1, f"{player[1]}({player[2]})")
        frame.pack(side=TOP, fill=X)
        label1.pack()
        label2.pack()
        label3.pack()
        listbox.pack()
        # exit_btn.pack()

    def close(self):
        self.send_and_receive_data({'purpose': 'dis-connecting', 'client-id':self.client_id})
        # quit()
        

if __name__=='__main__':
    client_number = input('Enter client number: ')

    if client_number=='1':
        client = Client("192.168.162.1", 30001, "192.168.162.1", 20000, "Rittwick 1", False)
    elif client_number=='2':
        client = Client("192.168.162.1", 30002, "192.168.162.1", 20000, "Rittwick 2", False)
    elif client_number=='3':
        client = Client("192.168.162.1", 30003, "192.168.162.1", 20000, "Rittwick 3", True, 2)
    elif client_number=='4':
        client = Client("192.168.162.1", 30004, "192.168.162.1", 20000, "Rittwick 4", True, 5)
    elif client_number=='5':
        client = Client("192.168.162.1", 30005, "192.168.162.1", 20000, "Rittwick 5", True, 10)
    else:
        client = Client(ip=gethostbyname(gethostname()))

    # threading.Thread(target=client.show).start()
    client.show()
