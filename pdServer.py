"""Server for pd application."""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle

def_control = {'PDxx':{'PA':0,'PB':0,'LED':0,'STYLE':0}}
clientLists = {}
ctrClients = {}

class Server:
    sock = socket(AF_INET,SOCK_STREAM)

    def __init__(self):
        self.sock.bind(('0.0.0.0',4000))
        self.sock.listen(1)

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            if not data:
                break
            else :
                if(data[6:10].decode("utf-8") not in clientLists):
                    clientLists[data[6:10].decode("utf-8")] = def_control['PDxx'].copy()
                    for sock in ctrClients:
                        data1 = pickle.dumps(clientLists)
                        sock.send(data1)

                c.send(data)
                #c.close()

        print("Model:"+data[0:6].decode("utf-8"), "ID:"+data[6:10].decode("utf-8"), end=" ")
        print("OP:0x{}".format(data[10]), "Dev:0x{}".format(data[11]), "Type:0x{}".format(data[12]), end=" ")
        if(data[13] != 0):
            print(data[14:].decode("utf-8"))
        else:
            print("HeartBeat")

    def run(self):
        while True:
            client, client_addr = self.sock.accept()
            cThread = Thread(args=(client, client_addr) , target=self.handler)
            cThread.daemon = True
            cThread.start()
            print('Server '+str(client_addr[0]) + ':' + str(client_addr[1]), ":", end='')

class CtrServer:
    sock = socket(AF_INET,SOCK_STREAM)

    def __init__(self):
        self.sock.bind(('0.0.0.0',4100))
        self.sock.listen(1)

    def handler(self, c, a):
        while True:
            data = c.recv(1024)
            if not data:
                break
            print(data.decode("utf-8"))

    def run(self):
        while True:
            client, client_addr = self.sock.accept()
            ctrClients[client] = client_addr[0]
            cThread = Thread(args=(client, client_addr) , target=self.handler)
            cThread.daemon = True
            cThread.start()
            print('ctrServer '+str(client_addr[0]) + ':' + str(client_addr[1]), ":", end='')


server = Server()
ctrserver = CtrServer()
ACCEPT_THREAD = Thread(target=server.run)
ACCEPT_THREAD1 = Thread(target=ctrserver.run)
ACCEPT_THREAD.start()
ACCEPT_THREAD1.start()
ACCEPT_THREAD.join()
ACCEPT_THREAD1.join()
server.sock.close()
CtrServer.sock.close()
