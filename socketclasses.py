# Erin Lavoie, Pearson Treanor, Nick Cameron
# MA398
# socketclasses.py

import socket as s
from Crypto.PublicKey import RSA
import threading
import AESCipher as aes
import pickle

class User:
    def __init__(self, controller, server_port=9019):
        self.port = server_port

        self.receiver = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.receiver.bind(("", self.port))

        self.sender = s.socket(s.AF_INET, s.SOCK_DGRAM)

        self.contacts = {}
        self.rsa = RSA.generate(2048)
        self.controller = controller
        threading_receive_message = threading.Thread(target=self.receive_message)
        threading_receive_message.start()

    def process_message(self, message, client_address):
        print("process message: ")
        print(message)
        if message == "":
            return
        elif self.contacts.get(client_address) is None:
            print("here")
            print(client_address)
            key = self.rsa.decrypt(message)
            self.contacts[client_address] = key
            print(key)
        else:
            key = self.contacts.get(client_address)
            dec = aes.decrypt(key, message)

            self.controller.display_message(dec, client_address)

    def contact_new_contact(self, client_address):
        my_pub = self.rsa.publickey()
        self.contacts[client_address] = None
        self.sender.sendto(pickle.dumps(my_pub), (client_address, self.port))
        #self.send_message(client_address, pickle.dumps(my_pub))

    def process_new_contact(self, message, client_address):
        client_pub = pickle.loads(message)
        key = aes.get_random_key()
        print("KEY: ")
        print(key)
        self.contacts[client_address] = key

        enc_key = client_pub.encrypt(key, 32)[0]

        self.sender.sendto(enc_key, (client_address, self.port))

        #self.send_message(client_address, enc_key)

        self.controller.new_contact(client_address)

    def receive_message(self):
        while True:
            message, client_address = self.receiver.recvfrom(2048)
            ip = client_address[0]

            if ip in self.contacts:
                self.process_message(message, ip)
            else:
                self.process_new_contact(message, ip)

    def send_message(self, contact, message):

        print(message)

        key = self.contacts.get(contact)
        print(self.contacts)
        enc = aes.encrypt(key, message)

        self.sender.sendto(enc, (contact, self.port))

class Controller:
    def __init__(self):
        self.id = "controller tester"

    def new_contact(self, contact):
        print("new contact: " + contact)

    def display_message(self, message):
        print("message recieved: " + message)


def main():
    tester = User(Controller())
    tester.contact_new_contact("127.0.0.1")
    tester.send_message("127.0.0.1", "Hello World")

if __name__=="__main__":
    main()