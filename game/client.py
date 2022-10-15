from datetime import datetime
from functools import partial
import time
from tkinter import * 
from socket import *
import threading 
import json 
from .shared.measurements.measurements import get_canvas_width, get_canvas_height, get_root_width, get_root_height, get_form_width, get_form_height, get_status_width, get_status_height, get_my_point_width, get_my_point_height, get_square_side_length

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
    """Client side of the application.

    Attributes:
        ip (str): ip address of client
        port (int): port of client
        buffer_size (int): buffer size of the client tcp connection.
        tcp_socket (socket.socket): tcp socket to talk with the server
        server_ip (str): ip address of the server
        server_port (int): port number of the server's tcp server.
        name (str): name of the client.
        points (int): score of the client.
        is_slow (bool): denotes whether the client is in slow network or not.
        delay (int): sends or receive the data after delay amount of time if the client is in a slow network.
        root (tk.Root): main window of the client.

    Methods:
        up_tcp_server: Starts the tcp server of the client side of the application in a different thread.
        tcp_server: TCP server of the client side.
        do_delay: Processes the data after delay amount of time if the client is in slow network.
        tcp_connection: TCP Connection of the client side.
        send_and_receive_data: Sends data to server and received the response from the server.
        make_form: Makes a blank form for the user to input the server address.
        draw_blank_canvas: Draws a blank canvas where the points will be in future to be clicked.
        blank_my_points: Draws a blank canvas where the points of a client will be shown.
        clear_canvas: Clear a canvas object
        write_on_canvas: Writes text on the (x,y) position of the canvas
        join_click_handler: This method is ran after the join button is clicked.
        draw_squares: Draws squares on the main canvas of the board.
        show: Shows the screen.
        update_point_canvas: Updates point-canvas and shows the score to client.
        square_click_handler: This method is invoked when user clicks on a square.
        on_game_end: This method is invoked when there is no more squares on the screen.
        handle_connections: This method is invoked on square is clicked.
        square_clicked: This square is clicked when the square is clicked.
        show_status: After the game over, server's data broadcast is handled by this method.
        show_final_status: Shows the final ranks of all of the players after the game is over.
        close: This method is invoked just before the client closes the window.    
    """

    def __init__(self, ip, port=30000, server_ip="", server_port=0, name="", is_slow=False, delay=5):
        """Constructor of the Client class

        Args:
            ip (str): ip address of the client
            port (int, optional): port number of the client. Defaults to 30000.
            server_ip (str, optional): ip address of the server. Defaults to "".
            server_port (int, optional): port number of the server. Defaults to 0.
            name (str, optional): name of the client. Defaults to "".
            is_slow (bool, optional): denotes if a client is in slow connection. Defaults to False.
            delay (int, optional): denotes the delay in seconds if the client is in a slow network. Defaults to 5.
        """

        self.ip = ip 
        self.port = port 
        self.buffer_size = 1024
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_socket.bind(("0.0.0.0", self.port))
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
        # self.root.geometry(f"{ROOT_WIDTH}x{ROOT_HEIGHT}")
        self.root.resizable(False, False)
        self.root.title('Real-time network multiplayer game')
        self.draw_blank_canvas()
        self.make_form()


    def up_tcp_server(self):
        """Starts the tcp server of the client side of the application in a different thread.
        """

        thread = threading.Thread(target=self.tcp_server)
        thread.start()
    
    def tcp_server(self):
        """TCP server of the client side.
        """

        print('TCP server is up in this client')
        while True:
            connection_socket, addr = self.tcp_socket.accept()
            thread = threading.Thread(target=self.tcp_connection, args=(connection_socket, addr))
            thread.start()
    
    def do_delay(self, data):
        """Processes the data after delay amount of time if the client is in slow network.

        Args:
            data (dictionary): The data dictionary sent from the server.
        """

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
        """TCP Connection of the client side.

        Args:
            connection_socket (socket.socket): connection socket of the client through which client will talk with the server
            addr (tuple): IP and Port tuple of the sender.
        """

        while True:
            data = connection_socket.recv(self.buffer_size).decode()
            print(f'The data is {data}')
            data = json.loads(data) 
            threading.Thread(target=self.do_delay, args=(data,)).start()

            
    def send_and_receive_data(self, data):
        """Sends data to server and received the response from the server.

        Args:
            data (dictionary): Data dictionary which has to be sent.

        Returns:
            dictionary: Response dictionary from server.
        """

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
        """Makes a blank form for the user to input the server address.

        """

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
        # name_entry.bind('<FocusOut>', partial(self.join_click_handler))

        ip_label.pack()
        ip_entry.pack()
        port_label.pack()
        port_entry.pack()
        name_label.pack()
        name_entry.pack()
        join_button.pack()
        self.form_frame.pack(anchor='nw', side=BOTTOM, pady=20, padx=15)
        self.ip_value.set(self.server_ip)
        self.port_value.set(self.server_port)
        self.name_value.set(self.name)

    def draw_blank_canvas(self):
        """Draws a blank canvas where the points will be in future to be clicked.
        """

        self.canvas = Canvas(self.root, height=CANVAS_HEIGHT, width=CANVAS_WIDTH, relief=GROOVE, borderwidth=2)
        self.canvas.pack(anchor=W) 
        self.write_on_canvas(self.canvas, 'To start the game enter the server IP address and port number.', CANVAS_WIDTH/2, CANVAS_HEIGHT/2)       

    def blank_my_points(self):
        """Draws a blank canvas where the points of a client will be shown.
        """

        self.points_canvas = Canvas(self.root, height=MY_POINT_HEIGHT, width=MY_POINT_WIDTH, relief=GROOVE, borderwidth=2)
        self.points_canvas.create_text(MY_POINT_WIDTH/2, MY_POINT_HEIGHT/2, text='My Points: 0')
        self.points_canvas.pack(anchor=E, side=RIGHT)

    def clear_canvas(self, canvas):
        """Clear a canvas object

        Args:
            canvas (tkinter.Canvas): An canvas object
        """

        try:
            canvas.delete('all') 
        except:
            pass 

    def write_on_canvas(self, canvas, text, x, y):
        """Writes text on the (x,y) position of the canvas

        Args:
            canvas (tkinter.Canvas): An canvas object
            text (str): The string to be written on the canvas
            x (int): x coordinate of the text
            y (int): y coordinate of the text
        """

        self.clear_canvas(canvas)
        try:
            canvas.create_text(x, y, text=text)
        except:
            pass 
    
    def join_click_handler(self, event):
        """This method is ran after the join button is clicked.

        Args:
            event (tkinter.Event): Button click event
        """

        # print('join request sent')
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
        """Draws squares on the main canvas of the board.
        """

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
        """Shows the screen.
        """

        self.root.mainloop()

    def update_point_canvas(self, new_point):
        """Updates point-canvas and shows the score to client.

        Args:
            new_point (int): user's score
        """

        self.clear_canvas(self.points_canvas)
        self.write_on_canvas(self.points_canvas, f'My Points: {new_point}', MY_POINT_WIDTH/2, MY_POINT_HEIGHT/2)

    def square_click_handler(self, event):
        """This method is invoked when user clicks on a square.

        Args:
            event (tkinter.Event): click event
        """

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
        """This method is invoked when there is no more squares on the screen.
        """

        self.clear_canvas(self.canvas)
        self.write_on_canvas(self.canvas, 'Game Over', CANVAS_WIDTH/2, CANVAS_HEIGHT/2)
        self.show_status()

    def handle_connections(self, square_id, clicked_at, amount=5):
        """This method is invoked on square is clicked.

        Args:
            square_id (int): id of the square
            clicked_at (datetime.datetime): the time when square is clicked.
            amount (int, optional): Score to increase. Defaults to 5.
        """

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
        """This square is clicked when the square is clicked.

        Args:
            square_id (int): id of the square
            clicked_at (datetime.datetime): time when square is clicked by the user.
            amount (int, optional): Score obtained by clicking on a square. Defaults to 5.
        """

        self.points = self.points + amount
        self.update_point_canvas(self.points)
        thread = threading.Thread(target=self.handle_connections, args=(square_id,clicked_at,amount))
        thread.start()

    def show_status(self):
        """After the game over, server's data broadcast is handled by this method.
        """

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
        """Shows the final ranks of all of the players after the game is over.

        Args:
            final_ranks (list): List of the players along with their rank and ids.
        """

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
        """This method is invoked just before the client closes the window.
        """

        print("Closing the client.")
        # self.send_and_receive_data({'purpose': 'dis-connecting', 'client-id':self.client_id})
        # quit()
        
def up_client():
    ip = input('Enter client ip address: ')
    port = int(input('Enter client port number: '))
    client = Client(ip, port)
    client.show()


if __name__=='__main__':
    client_number = input('Enter client number: ')
    # client_number = '1'

    if client_number=='1':
        client = Client("192.168.0.100", 30001, "192.168.0.100", 20000, "Rittwick 1", False)
    elif client_number=='2':
        client = Client("192.168.0.100", 30002, "192.168.0.100", 20000, "Rittwick 2", False)
    elif client_number=='3':
        client = Client("192.168.0.100", 30003, "192.168.0.100", 20000, "Rittwick 3", True, 2)
    elif client_number=='4':
        client = Client("192.168.0.100", 30004, "192.168.0.100", 20000, "Rittwick 4", True, 5)
    elif client_number=='5':
        client = Client("192.168.0.100", 30005, "192.168.0.100", 20000, "Rittwick 5", True, 10)
    else:
        ip = input('Enter you ip address (you can find it through your ipconfg or ifconfig command):')
        client = Client(ip=ip)

    # threading.Thread(target=client.show).start()
    client.show()
