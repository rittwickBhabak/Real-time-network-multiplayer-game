from datetime import datetime
from functools import partial
from tkinter import * 
import threading 
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

class GUI():
    """Front end GUI of the application.
    """

    def __init__(self):
        self.root = Tk()    
        self.root.geometry(f"{ROOT_WIDTH}x{ROOT_HEIGHT}")
        self.root.resizable(False, False)
        self.root.title('Real-time network multiplayer game')

        self.draw_blank_canvas()
        # self.make_blank_player_list()
        self.make_form()
        self.blank_my_points()
        
    def make_form(self):
        """Build the form to join the server

        Args:
            root (tkinter.Tk): reference of the main window
        """

        self.form_frame = Frame(self.root, borderwidth=2, relief=GROOVE,)
        ip_label = Label(self.form_frame, text="Enter Server IP address")
        port_label = Label(self.form_frame, text="Enter Server port number")
        name_label = Label(self.form_frame, text="Enter your name")
        self.ip_value = StringVar()
        self.port_value = StringVar()
        self.name_value = StringVar()
        # self.ip_value.set("127.0.0.2")
        # self.port_value.set("20001")
        # self.name_value.set("Rittwick")
        ip_entry = Entry(self.form_frame, textvariable=self.ip_value)
        port_entry = Entry(self.form_frame, textvariable=self.port_value)
        name_entry = Entry(self.form_frame, textvariable=self.name_value)

        join_button = Button(self.form_frame, text='Join Server')
        join_button.bind('<Button-1>', partial(self.join_click_handler))

        ip_label.pack(side=LEFT)
        ip_entry.pack(side=LEFT)
        port_label.pack(side=LEFT)
        port_entry.pack(side=LEFT)
        name_label.pack(side=LEFT)
        name_entry.pack(side=LEFT)
        join_button.pack(side=LEFT)
        self.form_frame.pack(anchor='nw', side=BOTTOM, pady=20, padx=15)

    def draw_blank_canvas(self):
        self.canvas = Canvas(self.root, height=CANVAS_HEIGHT, width=CANVAS_WIDTH, relief=GROOVE, borderwidth=2)
        self.canvas.pack(anchor=W) 
        self.write_on_canvas(self.canvas, 'To start the game enter the server IP address and port number.', CANVAS_WIDTH/2, CANVAS_HEIGHT/2)       

    def make_blank_player_list(self):
        self.players_frame = Frame(self.root, relief=GROOVE, borderwidth=2)
        heading = Label(self.players_frame, text='Players')
        self.players_list = Listbox(self.players_frame)
        self.players_frame.pack(side=RIGHT)
        heading.pack()
        self.players_list.pack()

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
                print(f'Square({square_id}) is clicked on {datetime.now()} by {self.client.player_id}')
                thread = threading.Thread(target=self.client.square_clicked, args=(square_id, datetime.now()))
                thread.start()
                if len(self.squares)==0:
                    print(f'Now there are no more squares')
                    thread = threading.Thread(target=self.on_game_end)
                    thread.start()

    def on_game_end(self):
        self.clear_canvas(self.canvas)
        self.write_on_canvas(self.canvas, 'Game Over', CANVAS_WIDTH/2, CANVAS_HEIGHT/2)
        self.client.show_status()

    def show_final_status(self, final_ranks):
        self.canvas.destroy()
        self.points_canvas.destroy()
        # self.players_frame.destroy()
        frame = Frame(self.root, relief=GROOVE, borderwidth=2, padx=20, pady=20)
        label1 = Label(frame, text="Game Over", font='times 24 bold')
        label2 = Label(frame, text=f"Your Points {self.client.points}", font='times 24 bold')
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
        exit_btn.pack()

    def close(self):
        self.client.close_client()
        quit()

    def update_point_canvas(self, new_point):
        self.clear_canvas(self.points_canvas)
        self.write_on_canvas(self.points_canvas, f'My Points: {new_point}', MY_POINT_WIDTH/2, MY_POINT_HEIGHT/2)

    def update_player_list(self, players, event=None):
        self.players_list.delete(0, END)
        players.sort(key=lambda x: x[2], reverse=True)
        for index, player in enumerate(players):
            self.players_list.insert(index+1, f'{player[1]}({player[2]})')

    def join_click_handler(self, event):
        ip = self.ip_value.get()
        port = self.port_value.get()
        name = self.name_value.get()
        # print(ip, port, name)
        (game_starts_at, coordinates) = self.client.connect_to_server(ip, port, name)

        self.coordinates = coordinates
        self.game_starts_at = game_starts_at

        self.form_frame.destroy() 

        self.draw_squares()

    def draw_squares(self):
        self.clear_canvas(self.canvas)
        # colors = ['red', 'green', 'blue', 'pink', 'yellow', 'black', 'maroon', 'purple', 'cyan', 'magenta']
        self.squares = []
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

    def set_client(self, client):
        self.client = client 
        print(client.serverIp, client.serverPort)
        self.ip_value.set(client.serverIp)
        self.port_value.set(client.serverPort)  

