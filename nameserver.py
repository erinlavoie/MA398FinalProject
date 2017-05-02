# Erin Lavoie, Pearson Treanor, Nick Cameron
# MA398
# nameserver.py

import socketclasses as nw
import threading

class Nameserver:

    def __init__(self):
        self.server = nw.Server()

        self.names = {}

        self.clients = []

        # set up message listener thread
        thread_receive_message = threading.Thread(target=self.receive_message)
        thread_receive_message.start()

        thread_send_message = threading.Thread(target=self.send_message)
        thread_send_message.start()

    def get_names(self):
        result = ""
        for user in self.names.keys():
            result += user + "\n"
        return result

    def receive_message(self):
        print("Now ready to receive messages")
        while True:
            message, client_address = self.server.receive_message()
            if message != "":
                self.process_message(message.decode(), client_address)

    def process_message(self, message, addr):
        self.names[message] = addr
        self.clients.append(nw.Client(addr))

    def send_message(self):
        names = self.get_names()
        for client in self.clients:
            client.send_message(names)


def main():
    Nameserver()

if __name__=="__main__":
    main()
