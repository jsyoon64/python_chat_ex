import socket
import threading
import pickle

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def sendMsg(self):
        while True:
            id = input("")
            if id == 'quit':
                self.sock.close()
                break

            else:
                data = 'SPP-CG' + id + '    '
                # self.sock.send(bytes(input(""), 'utf-8'))
                self.sock.send(bytes(data, 'utf-8'))

    def __init__(self, address):
        self.sock.connect(address)

        iThread = threading.Thread(target=self.sendMsg)
        iThread.daemon = True
        iThread.start()

        while True:
            data = self.sock.recv(1024)
            if not data:
                break

            if(PORT == 4100):
                data1 = pickle.loads(data)
                print(data1)
            else:
                print(data)


HOST = 'localhost'
PORT = input('Enter port: ')
PORT = int(PORT)

ADDR = (HOST, PORT)
client = Client(ADDR)
