import socket
import threading
import sys

class Server:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    connections = []
    def __init__(self):
        self.sock.bind(('0.0.0.0',3000))
        self.sock.listen(1)

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(data)
            if not data:
                print(str(a[0]) + ':' + str(a[1]), "disconnected")
                self.connections.remove(c)
                c.close()
                break

    def run(self):
        while True:
            c, a = self.sock.accept()
            cThread = threading.Thread(args=(c,a), target=self.handler)
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            print(str(a[0]) + ':' + str(a[1]), "connected")

class Client:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        def sendMsg(self):
            while True:
                self.sock.send(bytes(input(""), 'utf-8'))

        def __init__(self, address):
            self.sock.connect((address,3000))

            iThread = threading.Thread(target=self.sendMsg)
            iThread.daemon = True
            iThread.start()

            while True:
                data = self.sock.recv(1024)
                if not data:
                    break
                print(data)

if (len(sys.argv) > 1):
    #print(sys.argv[1])
    client = Client(sys.argv[1])
else:
    sever = Server()
    sever.run()
