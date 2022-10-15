"""This is the server side of the application."""

import datetime
import json
from socket import *
import threading
import random 

from .database import Database 
from .shared.measurements.measurements import *

CANVAS_WIDTH = get_canvas_width()
CANVAS_HEIGHT = get_canvas_height()
SQUARE_SIDE_LENGTH = get_square_side_length()

def generate_points(width, height, side_len, n=100):
    """Generate random , non-overlapping n points on the canvas.

    Args:
        width (int): Width of the canvas
        height (int): Height of the canvas
        side_len (int): side length of a square
        n (int, optional): Number of points on the canvas initially. Defaults to 100.

    Returns:
        (list): The list of top-left points of squares along with the ids
    """

    count = 0
    points = []
    colors = ['AliceBlue', 'AntiqueWhite', 'AntiqueWhite1', 'AntiqueWhite2', 'AntiqueWhite3', 'AntiqueWhite4', 'aquamarine', 'aquamarine1', 'aquamarine2', 'aquamarine3', 'aquamarine4', 'azure', 'azure1', 'azure2', 'azure3', 'azure4', 'beige', 'bisque', 'bisque1', 'bisque2', 'bisque3', 'bisque4', 'black', 'BlanchedAlmond', 'blue', 'blue', 'blue1', 'blue2', 'blue3', 'blue4', 'BlueViolet', 'brown', 'brown1', 'brown2', 'brown3', 'brown4', 'burlywood', 'burlywood1', 'burlywood2', 'burlywood3', 'burlywood4', 'CadetBlue', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3', 'CadetBlue4', 'chartreuse', 'chartreuse1', 'chartreuse2', 'chartreuse3', 'chartreuse4', 'chocolate', 'chocolate1', 'chocolate2', 'chocolate3', 'chocolate4', 'coral', 'coral1', 'coral2', 'coral3', 'coral4', 'CornflowerBlue', 'cornsilk', 'cornsilk1', 'cornsilk2', 'cornsilk3', 'cornsilk4', 'cyan', 'cyan1', 'cyan2', 'cyan3', 'cyan4', 'DarkBlue', 'DarkCyan', 'DarkGoldenrod', 'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4', 'DarkGray', 'DarkGreen', 'DarkGrey', 'DarkKhaki', 'DarkMagenta', 'DarkOliveGreen', 'DarkOliveGreen1', 'DarkOliveGreen2', 'DarkOliveGreen3', 'DarkOliveGreen4', 'DarkOrange', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4', 'DarkOrchid', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4', 'DarkRed', 'DarkSalmon', 'DarkSeaGreen', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3', 'DarkSeaGreen4', 'DarkSlateBlue', 'DarkSlateGray', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4', 'DarkSlateGrey', 'DarkTurquoise', 'DarkViolet', 'DeepPink', 'DeepPink1', 'DeepPink2', 'DeepPink3', 'DeepPink4', 'DeepSkyBlue', 'DeepSkyBlue1', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4', 'DimGray', 'DimGrey', 'DodgerBlue', 'DodgerBlue1', 'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'firebrick', 'firebrick1', 'firebrick2', 'firebrick3', 'firebrick4', 'FloralWhite', 'ForestGreen', 'fuchsia', 'gainsboro', 'GhostWhite', 'gold', 'gold1', 'gold2', 'gold3', 'gold4', 'goldenrod', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4', 'gray', 'gray0', 'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10', 'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19', 'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28', 'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37', 'gray38', 'gray39', 'gray40', 'gray41', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47', 'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56', 'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65', 'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74', 'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83', 'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92', 'gray93', 'gray94', 'gray95', 'gray96', 'gray97', 'gray98', 'gray99', 'gray100', 'green', 'green', 'green1', 'green2', 'green3', 'green4', 'GreenYellow', 'grey', 'grey0', 'grey1', 'grey2', 'grey3', 'grey4', 'grey5', 'grey6', 'grey7', 'grey8', 'grey9', 'grey10', 'grey11', 'grey12', 'grey13', 'grey14', 'grey15', 'grey16', 'grey17', 'grey18', 'grey19', 'grey20', 'grey21', 'grey22', 'grey23', 'grey24', 'grey25', 'grey26', 'grey27', 'grey28', 'grey29', 'grey30', 'grey31', 'grey32', 'grey33', 'grey34', 'grey35', 'grey36', 'grey37', 'grey38', 'grey39', 'grey40', 'grey41', 'grey42', 'grey43', 'grey44', 'grey45', 'grey46', 'grey47', 'grey48', 'grey49', 'grey50', 'grey51', 'grey52', 'grey53', 'grey54', 'grey55', 'grey56', 'grey57', 'grey58', 'grey59', 'grey60', 'grey61', 'grey62', 'grey63', 'grey64', 'grey65', 'grey66', 'grey67', 'grey68', 'grey69', 'grey70', 'grey71', 'grey72', 'grey73', 'grey74', 'grey75', 'grey76', 'grey77', 'grey78', 'grey79', 'grey80', 'grey81', 'grey82', 'grey83', 'grey84', 'grey85', 'grey86', 'grey87', 'grey88', 'grey89', 'grey90', 'grey91', 'grey92', 'grey93', 'grey94', 'grey95', 'grey96', 'grey97', 'grey98', 'grey99', 'grey100', 'honeydew', 'honeydew1', 'honeydew2', 'honeydew3', 'honeydew4', 'HotPink', 'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'IndianRed', 'IndianRed1', 'IndianRed2', 'IndianRed3', 'IndianRed4', 'indigo', 'ivory', 'ivory1', 'ivory2', 'ivory3', 'ivory4', 'khaki', 'khaki1', 'khaki2', 'khaki3', 'khaki4', 'lavender', 'lavender', 'LavenderBlush', 'LavenderBlush1', 'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'LawnGreen', 'LemonChiffon', 'LemonChiffon1', 'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'LightBlue', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4', 'LightCoral', 'LightCyan', 'LightCyan1', 'LightCyan2', 'LightCyan3', 'LightCyan4', 'LightGoldenrod', 'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4', 'LightGoldenrodYellow', 'LightGray', 'LightGreen', 'LightGrey', 'LightPink', 'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'LightSalmon', 'LightSalmon1', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'LightSeaGreen', 'LightSkyBlue', 'LightSkyBlue1', 'LightSkyBlue2', 'LightSkyBlue3', 'LightSkyBlue4', 'LightSlateBlue', 'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3', 'LightSteelBlue4', 'LightYellow', 'LightYellow1', 'LightYellow2', 'LightYellow3', 'LightYellow4', 'lime', 'lime', 'LimeGreen', 'linen', 'magenta', 'magenta1', 'magenta2', 'magenta3', 'magenta4', 'maroon', 'maroon1', 'maroon2', 'maroon3', 'maroon4', 'MediumAquamarine', 'MediumBlue', 'MediumOrchid', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3', 'MediumOrchid4', 'MediumPurple', 'MediumPurple1', 'MediumPurple2', 'MediumPurple3', 'MediumPurple4', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen', 'MediumTurquoise', 'MediumVioletRed', 'MidnightBlue', 'MintCream', 'MistyRose', 'MistyRose1', 'MistyRose2', 'MistyRose3', 'MistyRose4', 'moccasin', 'NavajoWhite', 'NavajoWhite1', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4', 'navy', 'navy', 'NavyBlue', 'OldLace', 'olive', 'olive', 'OliveDrab', 'OliveDrab1', 'OliveDrab2', 'OliveDrab3', 'OliveDrab4', 'orange', 'orange', 'orange1', 'orange2', 'orange3', 'orange4', 'OrangeRed', 'OrangeRed1', 'OrangeRed2', 'OrangeRed3', 'OrangeRed4', 'orchid', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'PaleGoldenrod', 'PaleGreen', 'PaleGreen1', 'PaleGreen2', 'PaleGreen3', 'PaleGreen4', 'PaleTurquoise', 'PaleTurquoise1', 'PaleTurquoise2', 'PaleTurquoise3', 'PaleTurquoise4', 'PaleVioletRed', 'PaleVioletRed1', 'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'PapayaWhip', 'PeachPuff', 'PeachPuff1', 'PeachPuff2', 'PeachPuff3', 'PeachPuff4', 'peru', 'pink', 'pink1', 'pink2', 'pink3', 'pink4', 'plum', 'plum1', 'plum2', 'plum3', 'plum4', 'PowderBlue', 'purple', 'purple1', 'purple2', 'purple3', 'purple4', 'red', 'red1', 'red2', 'red3', 'red4', 'RosyBrown', 'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'RoyalBlue', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'SaddleBrown', 'salmon', 'salmon1', 'salmon2', 'salmon3', 'salmon4', 'SandyBrown', 'SeaGreen', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'SeaGreen4', 'seashell', 'seashell1', 'seashell2', 'seashell3', 'seashell4', 'sienna', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'silver', 'SkyBlue', 'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'SlateBlue', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3', 'SlateBlue4', 'SlateGray', 'SlateGray1', 'SlateGray2', 'SlateGray3', 'SlateGray4', 'SlateGrey', 'snow', 'snow1', 'snow2', 'snow3', 'snow4', 'SpringGreen', 'SpringGreen1', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4', 'SteelBlue', 'SteelBlue1', 'SteelBlue2', 'SteelBlue3', 'SteelBlue4', 'tan', 'tan1', 'tan2', 'tan3', 'tan4', 'teal', 'thistle', 'thistle1', 'thistle2', 'thistle3', 'thistle4', 'tomato', 'tomato1', 'tomato2', 'tomato3', 'tomato4', 'turquoise', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'violet', 'violet', 'VioletRed', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4', 'wheat', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'white', 'white', 'WhiteSmoke', 'yellow', 'yellow', 'yellow1', 'yellow2', 'yellow3', 'yellow4', 'YellowGreen']

    while count<n:
        x0 = random.randint(40,width-40)
        y0 = random.randint(40,height-40)

        flag = True 
        for point in points:
            _x = point.get('x0') 
            _y = point.get('y0') 
            if (_x-side_len<=x0<=_x+2*side_len and _y-side_len<=y0<=_y+2*side_len) \
                or (_x-side_len<=x0+side_len<=_x+2*side_len and _y-side_len<=y0+side_len<=_y+2*side_len):
                flag = False 
                break 
        if flag:
            points.append({'_id':count, 'id':count, 'x0':x0, 'y0':y0, 'color':random.choice(colors)})
            count = count + 1



    return points


class Server():
    """This is the server of the application. This acts as an central authority.
    """

    def __init__(self, ip, port, number_of_points=5, start_match_after=10):
        """Constructor of the Server class in which one tcp server is running.

        Args:
            ip (str): ip address of the server's tcp server
            port (int): port number of the server's tcp server
            number_of_points (int, optional): Number of squares on the board. Defaults to 5.
            start_match_after (datetime.datetime, optional): Seconds, after this amount of seconds since the server starts the points will be drawn on the canvas of the clients. Defaults to 10.
        """

        self.ip = ip 
        self.port = port 
        self.buffer_size = 1024
        self.tcp_socket = socket(AF_INET, SOCK_STREAM)
        self.tcp_socket.bind((self.ip, self.port))
        self.tcp_socket.listen(100)
        print(f'Server address {self.ip}:{self.port}')
        self.up_tcp_server()
        self.clients = [] 
        self.database = Database()
        self.game_starts_at = datetime.datetime.now() + datetime.timedelta(seconds=start_match_after)
        self.coordinates = generate_points(CANVAS_WIDTH, CANVAS_HEIGHT, SQUARE_SIDE_LENGTH, number_of_points)
        self.database.insert_points(self.coordinates)

    def up_tcp_server(self):
        """Starting up an TCP server on a different thread of the client.
        """

        thread = threading.Thread(target=self.tcp_server)
        thread.start()
    
    def tcp_server(self):
        """TCP Server of the client side.
        """

        while True:
            connection_socket, addr = self.tcp_socket.accept()
            thread = threading.Thread(target=self.tcp_connection, args=(connection_socket, addr))
            thread.start()
    
    def tcp_connection(self, connection_socket, addr):
        """This TCP connection analyzes the data came from client and send appropriate messages to the clients.

        Args:
            connection_socket (socket.socket): Through this socket the communication happens.
            addr (tuple): The ip address and port number of the server.
        """
        
        while True:
            data = connection_socket.recv(self.buffer_size).decode()
            data = json.loads(data) 
            purpose = data.get('purpose')
            print(f'The purpose of the data is {purpose}')

            # {'purpose':'join-req', 'name':self.name, 'client-tcp-ip':self.ip, 'client-tcp-port':self.port}
            # {'client-id', 'coordinates', 'game-starts-at'}
            if purpose=='join-req':
                client_id = len(self.clients) + 1 
                name = data.get('name')
                client_tcp_ip = data.get('client-tcp-ip')
                client_tcp_port = data.get('client-tcp-port')
                client_tcp_socket = socket(AF_INET, SOCK_STREAM)
                client_tcp_socket.connect((client_tcp_ip, client_tcp_port))
                client_obj = {'id':client_id, 'name':name, 'client-tcp-socket':client_tcp_socket}
                self.clients.append(client_obj)
                self.database.insert_player({'id':client_id, 'name':name, 'points':0})

                response_obj = {'client-id':client_id, 'coordinates':self.coordinates, 'game-starts-at':str(self.game_starts_at)}
                response_obj = json.dumps(response_obj)
                connection_socket.send(response_obj.encode())

            # {'purpose': 'square-click', 'square-id': square_id, 'clicked-at':clicked_at, 'clicked-by':client_id}
            # {'actually-clicked-by'}
            elif purpose=='square-click':
                square_id = data.get('square-id')
                clicked_at = data.get('clicked-at')
                clicked_by = data.get('clicked-by')

                (previously_clicked_by, actually_clicked_by) = self.database.find_square_id(square_id, clicked_by, clicked_at)
                response_obj = {'actually-clicked-by':actually_clicked_by}
                response_obj = json.dumps(response_obj)
                connection_socket.send(response_obj.encode())

                if previously_clicked_by!=actually_clicked_by :
                    print(f'square({square_id}) was previously clicked by {previously_clicked_by}')
                    for c in self.clients:
                        if c.get('id')==previously_clicked_by:
                            message = {'purpose':'update-points'}
                            message = json.dumps(message)
                            c.get('client-tcp-socket').send(message.encode())

                # broadcast the message 
                broadcast_message = {'purpose':'delete-square', 'square-id':square_id}
                broadcast_message = json.dumps(broadcast_message)
                for c in self.clients:
                    c_id = c.get('id')
                    if client_id!=c_id:
                        c_tcp_socket = c.get('client-tcp-socket')
                        c_tcp_socket.send(broadcast_message.encode())

            # {'purpose': 'gave-over', 'client-id':client_id}
            elif purpose=='game-over':
                client_id = data.get('client-id')
                flag = self.database.game_over_request(client_id)
                if flag==False:
                    connection_socket.send(json.dumps({'purpose':'wait'}).encode())
                else:
                    final_ranks = self.database.get_final_ranks()
                    broadcast_message = {'purpose':'game-over', 'final-ranks':final_ranks}
                    broadcast_message = json.dumps(broadcast_message)
                    connection_socket.send(broadcast_message.encode())

                    for c in self.clients:
                        c_id = c.get('id')
                        if client_id!=c_id:
                            c.get('client-tcp-socket').send(broadcast_message.encode())

                
            # {'purpose': 'dis-connecting', 'client-id':client_id}
            elif purpose=='dis-connecting':
                client_id = data.get('client-id')
                connection_socket.send(json.dumps({'purpose':'quit'}).encode())
                for c in self.clients:
                    if c.get('id')==client_id:
                        c.get('client-tcp-socket').close()
                        more_clients = self.database.decrease_player(client_id)
                        if more_clients==0:
                            print(f'Number of clients {more_clients}')
                            # exit(1)
def up_server():
    ip = input('Enter server ip address: ')
    port = 20000
    number_of_points=int(input('Enter number of points on the screen: '))
    start_match_after = int(input('How many seconds after starting the server the game will begin: '))
    Server(ip, port, number_of_points,start_match_after)

if __name__=='__main__':
    server = Server(gethostbyname(gethostname()), 20000, number_of_points=5, start_match_after=10)
