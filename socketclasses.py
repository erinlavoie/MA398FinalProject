# Erin Lavoie, Pearson Treanor, Nick Cameron
# MA398
# socketclasses.py

import socket as s
from Crypto.PublicKey import RSA
import threading
import AESCipher as aes
import pickle
import time


class User:
    def __init__(self, controller, server_port=12000):
        self.port = server_port

        self.receiver = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.receiver.bind(("", self.port))

        self.sender = s.socket(s.AF_INET, s.SOCK_DGRAM)

        self.contacts = {}
        self.rsa = RSA.generate(2048)
        self.controller = controller
        threading_receive_message = threading.Thread(target=self.receive_message)
        threading_receive_message.start()

    def reset_keys(self):
        self.rsa = RSA.generate(2048)

    def process_message(self, message, client_address):

        print("processing message < " + str(message) + " > from " + client_address)

        if message == "":
            return

        elif self.contacts.get(client_address) is None:
            key = self.rsa.decrypt(message)
            self.contacts[client_address] = key

        else:
            key = self.contacts.get(client_address)
            dec = aes.decrypt(key, message)

            self.controller.display_message(dec, client_address)

    def contact_new_contact(self, client_address):
        print("Contacting a new contact: " + client_address)
        my_pub = self.rsa.publickey()
        self.contacts[client_address] = None
        self.sender.sendto(pickle.dumps(my_pub), (client_address, self.port))

    def process_new_contact(self, message, client_address):
        print("processing a new contact: " + client_address)
        client_pub = pickle.loads(message)
        print(type(client_pub))
        print("generating a random key")
        key = aes.get_random_key()
        print("key: " + str(key))
        self.contacts[client_address] = key
        print("populating contacts.")
        enc_key = client_pub.encrypt(key, 32)[0]

        self.sender.sendto(enc_key, (client_address, self.port))

        self.controller.new_contact2(client_address)

    def receive_message(self):
        while True:
            message, client_address = self.receiver.recvfrom(2048)
            print(client_address)
            print(self.contacts)
            ip = client_address[0]
            if message == "":
                continue
            print(str(ip) + "'s message: " + str(message) + " was received")
            if ip in self.contacts: #and type(pickle.loads(message)) is not 'Crypto.PublicKey.RSA._RSAobj':
                self.process_message(message, ip)
            else:
                self.process_new_contact(message, ip)

    def send_message(self, contact, message):
        if self.contacts.get(contact) is not None:
            key = self.contacts.get(contact)

            enc = aes.encrypt(key, message)

            self.sender.sendto(enc, (contact, self.port))

class Controller:
    def __init__(self):
        self.id = "controller tester"

    def new_contact(self, contact):
        print("new contact: " + contact)

    def display_message(self, message):
        print("message recieved: " + message)

    def new_contact2(self, contact):
        print("new contact2: " + contact)


def main():
    tester = User(Controller())
    #tester.contact_new_contact("137.146.127.19")
    # time.sleep(30)
    # tester.send_message("137.146.140.49", "PLZ WORK")



if __name__=="__main__":
    main()