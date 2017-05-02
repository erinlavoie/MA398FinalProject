# Erin Lavoie, Pearson Treanor, Nick Cameron
# MA398
# socketclasses.py

import socket as s
import threading

class Client:
    def __init__(self, dest_server_name, dest_server_port=12000):
        self.dest_server_name = dest_server_name
        self.dest_server_port = dest_server_port
        self.client_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        #self.establish_connection()

    def establish_connection(self):
        print("Establishing connection")
        self.client_socket.sendto('HELLO'.encode(), (self.dest_server_name, self.dest_server_port))
        response = self.client_socket.recvfrom(2048)
        if response[0].decode() == 'ACK':
            print("Connection established")
        else:
            print("Connection failed")

    def send_message(self, message):
        self.client_socket.sendto(message.encode(), (self.dest_server_name, self.dest_server_port))
        #print(message)


class Server:
    def __init__(self, server_port=12000):
        print("Setting up server")
        self.server_port = server_port
        self.server_socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.server_socket.bind(('', self.server_port))
        self.ACK = 'ACK'.encode()

    def receive_message(self):
        message, client_address = self.server_socket.recvfrom(2048)
        return message, client_address

class User:
    def __init__(self, controller, dst_server_name='localhost', server_port=12000, dst_server_port=12000):
        self.controller = controller
        self.message = ""

        # init local server
        self.server = Server(server_port)
        # set up message listener thread
        thread_recieve_message = threading.Thread(target=self.receive_message)
        thread_recieve_message.start()

        # init client
        self.client = Client(dst_server_name, dst_server_port)
        # set up message sender thread
        thread_send_message = threading.Thread(target=self.send_message)
        thread_send_message.start()

    def set_message(self, message):
        self.message = message

    def send_message(self):
        while True:
            self.client.send_message(self.message)
            self.message = ""

    def receive_message(self):
        print("Now ready to recieve messages")
        while True:
            message, client_address = self.server.receive_message()
            self.controller.handle_receive(self, message.decode())
